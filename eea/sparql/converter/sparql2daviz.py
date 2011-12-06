def sparql2json(data):
    items = []

    columns = [column_type(col) for col in data['var_names']]

    properties = {}
#    properties = dict (columns)
    for column in columns:
        properties[column[0].encode('utf8')] = {'value_type':column[1].encode('utf8')}
    index = 0
    for row in data['rows']:
        index += 1
        rowdata = {}
        rowdata['label'] = index
        itemindex = 0
        for item in row:
            if item:
                rowdata[columns[itemindex][0].encode('utf8')] = item.value.encode('utf8')
            else:
                rowdata[columns[itemindex][0].encode('utf8')] = ''
            itemindex += 1
        items.append(rowdata)
    return {'items': items, 'properties': properties}


def column_type(column):
    if "_type" not in column:
        return column, "text"
    return column.split("_type")[0], column.split("_type")[-1]