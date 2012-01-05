""" sparql
"""
from Products.Five import BrowserView
from Products.ZSPARQLMethod.Method import parse_arg_spec, map_arg_values, \
                                        interpolate_query_html
from time import time
import json

from eea.sparql.converter.sparql2json import sparql2json

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
