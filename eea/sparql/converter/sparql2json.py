"""
Helper functions to convert sparql data to json json

    >>> from eea.sparql.converter import sparql2json
    >>> from eea.sparql.tests import mock_data
    >>> test_data = mock_data.loadSparql()
    >>> type(test_data)
    <type 'dict'>

"""

from eea.sparql.converter import mixin

from Products.ZSPARQLMethod.Method import MethodResult

def sparql2json(data):
    """ Returns JSON output after converting source data
        >>> data = sparql2json.sparql2json(test_data)
        >>> print (data['items'])
        [{'available': True,
        'name': 'Name1',
        'tags': [u'a', u'b', u'c', u'd'],
        'url': 'http://www.url1.com',
        'age': 30,
        'label': 1},
        {'available': False,
        'name': 'Name2',
        'tags': [u'single item'],
        'url': 'http://www.url2.com',
        'age': 25,
        'label': 2},
        {'available': False,
        'name': 'Name3',
        'tags': [],
        'url': '',
        'age': 0,
        'label': 3}]

    """

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
        rowdata = {}
        if not hasLabel:
            rowdata['label'] = index
        idx = 0
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

            rowdata[cols[idx][0].encode('utf8')] = value

            idx += 1
        items.append(rowdata)
    return {'items': items, 'properties': properties}

def sparql2json2(data):
    items = []
    hasLabel = False
    mr = MethodResult(data)
    cols = mr.var_names

    properties = {}
    for col in cols:
        if col.lower().endswith("label"):
            col = 'label'
            hasLabel = True
        properties[col] = 'text'

    index = 0
    for row in mr:
        index += 1
        rowdata = {}
        if not hasLabel:
            rowdata['label'] = index
        idx = 0
        for item in row:
            rowdata[cols[idx]] = item
            idx += 1
        items.append(rowdata)
    return {'items': items, 'properties': properties}
