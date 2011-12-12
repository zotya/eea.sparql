import os
import json
from StringIO import StringIO
import sparql

def loadSparql():
    json_file = os.path.join(os.path.dirname(__file__),"sparql.json")
    f = open(json_file, 'r')
    json_str = f.read()
    f.close()
    io = StringIO(json_str)
    json_data = json.load(io)

    data = {}
    data['var_names'] = json_data['var_names']
    data['rows'] = []
    for row in json_data['rows']:
        datarow = []
        for col in json_data['var_names']:
            value = None
            if row[col]:
                value = sparql.Literal(row[col])
            datarow.append(value)
        data['rows'].append(datarow)
    return data
