""" sparql
"""

from Products.Five import BrowserView
from Products.ZSPARQLMethod.Method import interpolate_query_html
from Products.ZSPARQLMethod.Method import map_arg_values
from Products.ZSPARQLMethod.Method import parse_arg_spec
from eea.sparql.converter.sparql2json import sparql2json
from Products.statusmessages.interfaces import IStatusMessage
from lovely.memcached.event import InvalidateCacheEvent
from time import time
from zope.event import notify
import hashlib
import json
import urllib2

class Sparql(BrowserView):
    """Sparql view"""

    def test_query(self):
        """test query"""
        arg_spec = parse_arg_spec(self.context.arg_spec)
        missing, arg_values = map_arg_values(arg_spec, self.request.form)
        error = None

        if missing:
            # missing argument
            data = None
            dt = 0

        else:
            t0 = time()

            try:
                data = self.context.execute(**arg_values)

            except Exception:
                import traceback
                error = traceback.format_exc()
                data = None

            dt = time() - t0

        options = {
            'query': interpolate_query_html(self.context.query, arg_values),
            'data': data,
            'duration': dt,
            'arg_spec': arg_spec,
            'error': error,
        }

        return options

    def json(self):
        """json"""
        data = self.context.execute_query()
        return json.dumps(sparql2json(data))

    def sparql_download(self):
        format = self.request['format']
        title = self.context.title
        if format in ['exhibit', 'html', 'tsv', 'csv']:
            data = self.context.execute_query()
            jsonData = sparql2json(data)
            result = ''

            if format == 'exhibit':
                self.request.response.setHeader('Content-Type', 'application/json')
                self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s.json"' %title)
                result = json.dumps(jsonData)

            if format == 'html':
                result += "<style type='text/css'>\r\n"
                result += "table{border-collapse:collapse}\r\n"
                result += "th,td {border:1px solid black}\r\n"
                result += "</style>\r\n"
                result += "<table>\r\n"
                result += "\t<tr>\r\n"
                for col in jsonData['properties'].keys():
                    result += "\t\t<th>" + col + "</th>\r\n"
                result += "\t</tr>\r\n"
                for row in jsonData['items']:
                    result += "\t<tr>\r\n"
                    for col in jsonData['properties'].keys():
                        result += "\t\t<td>" + str(row[col]) + "</td>\r\n"
                    result += "\t</tr>\r\n"
                result += "</table>\r\n"

            if format in ['csv', 'tsv']:
                self.request.response.setHeader('Content-Type', 'application/csv')
                self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s.csv"' %title)
                separator = ', '
                if format == 'tsv':
                    self.request.response.setHeader('Content-Type', 'application/tsv')
                    self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s.tsv"' %title)
                    separator = '\t'
                first = True
                for col in jsonData['properties'].keys():
                    if not first:
                        result += separator
                    result += col + ":" + jsonData['properties'][col]
                    first = False

                result += "\r\n"
                for row in jsonData['items']:
                    first = True
                    for col in jsonData['properties'].keys():
                        if not first:
                            result += separator
                        result += str(row[col])
                        first = False

                    result += "\r\n"

            return result

        if format in ['json', 'xml', 'xml_with_schema']:
            endpoint = self.context.endpoint_url
            query = 'query='+self.context.query
            headers = ''
            if format == 'json':
                headers = {'Accept' : 'application/sparql-results+json'}
                self.request.response.setHeader('Content-Type', 'application/json')
                self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s.json"' %title)

            if format == 'xml':
                headers = {'Accept' : 'application/sparql-results+xml'}
                self.request.response.setHeader('Content-Type', 'application/xml')
                self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s.xml"' %title)

            if format == 'xml_with_schema':
                headers = {'Accept' : 'application/x-ms-access-export+xml'}
                self.request.response.setHeader('Content-Type', 'application/xml')
                self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s.xml"' %title)

            request = urllib2.Request(endpoint, query, headers)
            results = urllib2.urlopen(request).fp.read()

            return results


class Caching(BrowserView):
    """ Caching for sparql query results """

    def __call__(self):
        if not "submit" in self.request.form:
            return self.index()

        c = self.context
        key = str(c.getArg_spec()) + str(c.getSparql_query())
        key = hashlib.md5(key).hexdigest()

        notify(InvalidateCacheEvent())

        IStatusMessage(self.request).addStatusMessage("Cache invalidated")
        return self.index()


