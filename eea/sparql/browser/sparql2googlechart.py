""" sparql2googlechart
"""
from Products.Five import BrowserView
from eea.sparql.converter.sparql2googlechart import sparql2json

class Sparql2GoogleChart(BrowserView):
    """Sparql2GoogleChart view"""
    def json(self):
        """json"""
        data = self.context.aq_parent.execute_query()
        return sparql2json(data)
