""" sparql2daviz
"""
import json
from Products.Five import BrowserView
from eea.sparql.converter.sparql2daviz import sparql2json

class Sparql2Daviz(BrowserView):
    """Sparql2Daviz view"""
    def json(self):
        """json"""
        data = self.context.aq_parent.execute_query()
        return json.dumps(sparql2json(data))
