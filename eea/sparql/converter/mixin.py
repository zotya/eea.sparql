"""
Helper functions to convert sparql data to json

    >>> from eea.sparql.converter import mixin
    >>> from eea.sparql.tests import mock_data
    >>> test_data = mock_data.loadSparql()
    >>> type(test_data)
    <type 'dict'>

"""

import logging
from Products.CMFPlone.utils import normalizeString

logger = logging.getLogger('eea.sparql.converter.mixin')

def item2text(value):
    """ Get utf8 string from value
        >>> mixin.item2text(u'sometext')
        'sometext'

        None value should return empty string
        >>> mixin.item2text(None)
        ''

    """
    if not value:
        return ''
    return value.encode('utf8')

def item2list(value):
    """ Detect lists in value

        Works with ","
        >>> mixin.item2list("Pig, Goat, Cow")
        ['Pig', 'Goat', 'Cow']

        Also with ";"
        >>> mixin.item2list("Pig; Goat; Cow")
        ['Pig', 'Goat', 'Cow']

        If it can't find any comma or semicolon it will return a list of one
        item
        >>> mixin.item2list("Pig")
        ['Pig']

        If the value is None, empty list will be returned
        >>> mixin.item2list(None)
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

        >>> mixin.item2number("2011")
        2011

        >>> mixin.item2number("9.99")
        9.9...

        It fails silently if the provided value is not a number
        >>> mixin.item2number("9-99")
        '9-99'

        If the value is None, 0 will be returned
        >>> mixin.item2number(None)
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

        >>> mixin.item2boolean("2011")
        True

        Be carefull, "False" is a True in python as it's not an emtry string
        >>> mixin.item2boolean("False")
        True

        So use :bool only when you test if value is empty or not
        >>> mixin.item2boolean("")
        False

        >>> mixin.item2boolean(None)
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
        >>> mixin.column_type("Start_typedate")
        ('start', 'date')

        >>> mixin.column_type("Website_typeurl")
        ('website', 'url')

        >>> mixin.column_type("Items_one_two_typelist")
        ('items_one_two', 'list')

        >>> mixin.column_type("Title")
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
        colname = "label"
    return colname, coltype

def getColumns(data):
    """ Returns the columns with their types 
        >>> columns = mixin.getColumns(test_data)
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

