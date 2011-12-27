"""Definition of the Sparql2GoogleChart content type
"""

from zope.event import notify
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata, base

from eea.googlechartsconfig.events import GoogleChartEnabledEvent
from eea.sparql.interfaces import ISparql2GoogleChart
from eea.sparql.config import PROJECTNAME
from eea.sparql.converter.sparql2googlechart import getColumns


Sparql2GoogleChartSchema = schemata.ATContentTypeSchema.copy()

Sparql2GoogleChartSchema['title'].storage = atapi.AnnotationStorage()
Sparql2GoogleChartSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(Sparql2GoogleChartSchema, moveDiscussion=False)

class Sparql2GoogleChart(base.ATCTContent):
    """Sparql2GoogleChart"""
    implements(ISparql2GoogleChart)

    meta_type = "Sparql2GoogleChart"
    schema = Sparql2GoogleChartSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


atapi.registerType(Sparql2GoogleChart, PROJECTNAME)

def handle_object_initialized(obj, event):
    """Handle object initialized"""
    sparqldata = obj.aq_parent.execute_query()
    columns = getColumns(sparqldata)

    notify(GoogleChartEnabledEvent(obj, columns=columns))
