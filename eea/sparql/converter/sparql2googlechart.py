"""
Helper functions to convert sparql data to googlechart json

    >>> from eea.sparql.converter import sparql2googlechart
    >>> from eea.sparql.tests import mock_data
    >>> test_data = mock_data.loadSparql()
    >>> type(test_data)
    <type 'dict'>

"""

import json
from eea.sparql.converter import mixin

def sparql2json(data):
    """ Returns JSON output after converting source data
        >>> data = sparql2googlechart.sparql2json(test_data)
        >>> import StringIO
        >>> import json
        >>> data = json.load(StringIO.StringIO(data))
        >>> print (data['dataTable'])
        [[u'Name1', u'http://www.url1.com', [u'a', u'b', u'c', u'd'], True, 30],
        [u'Name2', u'http://www.url2.com', [u'single item'], False, 25],
        [u'Name3', u'', [], False, 0]]

    """

    items = []
    cols = [mixin.column_type(col) for col in data['var_names']]

    properties = {}
    for col in cols:
        colname = col[0].encode('utf8')
        coltype = col[1].encode('utf8')
        properties[colname] = {'value_type':coltype}

    for row in data['rows']:
        idx = 0
        datarow = []
        for item in row:
            if not item:
                itemvalue = None
            else:
                itemvalue = item.value
            if cols[idx][1] == 'number':
                value = mixin.item2number(itemvalue)
            else:
                if cols[idx][1] == 'boolean':
                    value = mixin.item2boolean(itemvalue)
                else:
                    if cols[idx][1] == 'list':
                        value = mixin.item2list(itemvalue)
                    else:
                        value = mixin.item2text(itemvalue)

            datarow.append(value)
            idx += 1
        items.append(datarow)
    return json.dumps({"dataTable": items})

