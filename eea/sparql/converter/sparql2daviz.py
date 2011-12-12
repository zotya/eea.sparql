import logging
from Products.CMFPlone.utils import normalizeString

logger = logging.getLogger('eea.sparql.converter.sparql2daviz')

"""
    Helper functions to convert sparql data to json
    >>> from eea.sparql.converter import sparql2daviz
    >>> from eea.sparql.tests import mock_data
    >>> test_data = mock_data.loadSparql()

"""

def item2text(value):
    """ Get utf8 string from value
        >>> sparql2daviz.item2text(u'sometext')
        'sometext'

        None value should return empty string
        >>> sparql2daviz.item2text(None)
        ''

    """
    if not value:
        return ''
    return value.encode('utf8')

def item2list(value):
    """ Detect lists in value

        Works with ","
        >>> sparql2daviz.item2list("Pig, Goat, Cow")
        ['Pig', 'Goat', 'Cow']

        Also with ";"
        >>> sparql2daviz.item2list("Pig; Goat; Cow")
        ['Pig', 'Goat', 'Cow']

        If it can't find any comma or semicolon it will return a list of one
        item
        >>> sparql2daviz.item2list("Pig")
        ['Pig']

        If the value is None, empty list will be returned
        >>> sparql2daviz.item2list(None)
        []

    """

    if not value:
        return []

    if "," in value:
        value = value.split(",")
    elif ";" in value:
        value = value.split(";")
    else:
        value = [value, ]

    value = [item.strip() for item in value]
    return value

def item2number(value):
    """ Detect numbers in value

        >>> sparql2daviz.item2number("2011")
        2011

        >>> sparql2daviz.item2number("9.99")
        9.9...

        It fails silently if the provided value is not a number
        >>> sparql2daviz.item2number("9-99")
        '9-99'

        If the value is None, 0 will be returned
        >>> sparql2daviz.item2number(None)
        0

    """

    if not value:
        return 0

    try:
        value = int(value)
    except Exception:
        try:
            value = float(value)
        except Exception, err:
            logger.debug(err)
    return value

def item2boolean(value):
    """ Detect boolean in string

        >>> sparql2daviz.item2boolean("2011")
        True

        Be carefull, "False" is a True in python as it's not an emtry string
        >>> sparql2daviz.item2boolean("False")
        True

        So use :bool only when you test if value is empty or not
        >>> sparql2daviz.item2boolean("")
        False

        >>> sparql2daviz.item2boolean(None)
        False

        """
    try:
        value = bool(value)
    except Exception, err:
        logger.debug(err)
    return value

def column_type(column):
    """ Get column and type from column
        As a convention, if it's necessary, we set the type of column by adding:
        _type<typename>
        ex: col_typenumber, col_typeboolean, col_typelist, but the typename can 
        be anything. If it's missing, we consider it as text
        >>> sparql2daviz.column_type("Start_typedate")
        ('start', 'date')

        >>> sparql2daviz.column_type("Website_typeurl")
        ('website', 'url')

        >>> sparql2daviz.column_type("Items_one_two_typelist")
        ('items_one_two', 'list')

        >>> sparql2daviz.column_type("Title")
        ('title', 'text')

    """
    column = normalizeString(column, encoding='utf-8')
    if "_type" not in column:
        colname = column
        coltype = "text"
    else:
        colname = column.split("_type")[0]
        coltype = column.split("_type")[-1]
    if colname.lower().endswith("label"):
        colname = "label";
    return colname, coltype


def sparql2json(data):
    """ Returns JSON output after converting source data.
        >>> data = sparql2daviz.sparql2json(test_data)
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
    cols = [column_type(col) for col in data['var_names']]

    properties = {}
    for col in cols:
        colname = col[0].encode('utf8')
        coltype = col[1].encode('utf8')
        if colname == 'label':
            hasLabel = True
        properties[colname]= {'value_type':coltype}

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
                value = item2number(itemvalue)
            else:
                if cols[idx][1] == 'boolean':
                    value = item2boolean(itemvalue)
                else:
                    if cols[idx][1] == 'list':
                        value = item2list(itemvalue)
                    else:
                        value = item2text(itemvalue)

            rowdata[cols[idx][0].encode('utf8')] = value

            idx += 1
        items.append(rowdata)
    return {'items': items, 'properties': properties}

def getColumns(data):
    """ Returns the columns with their types 
        >>> columns = sparql2daviz.getColumns(test_data)
        >>> print columns.next()
        ('name', 'text')
        >>> print columns.next()
        ('url', 'url')
        >>> print columns.next()
        ('tags', 'list')
        >>> print columns.next()
        ('available', 'boolean')
        >>> print columns.next()
        ('age', 'number')

    """
    return (column_type(col) for col in data['var_names'])

