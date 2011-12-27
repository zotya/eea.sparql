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

    items = []
    hasLabel = False
    cols = [mixin.column_type(col) for col in data['var_names']]

    properties = {}
    for col in cols:
        colname = col[0].encode('utf8')
        coltype = col[1].encode('utf8')
        if colname == 'label':
            hasLabel = True
        properties[colname] = {'value_type':coltype}

    index = 0
    for row in data['rows']:
        index += 1
        if not hasLabel:
            rowdata['label'] = index
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

