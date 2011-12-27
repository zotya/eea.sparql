"""Definition of the Sparql2Daviz content type
"""

from zope.event import notify
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata, base

from eea.daviz.events import DavizEnabledEvent
from eea.sparql.interfaces import ISparql2Daviz
from eea.sparql.config import PROJECTNAME
from eea.sparql.converter.mixin import getColumns


Sparql2DavizSchema = schemata.ATContentTypeSchema.copy()

Sparql2DavizSchema['title'].storage = atapi.AnnotationStorage()
Sparql2DavizSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(Sparql2DavizSchema, moveDiscussion=False)

class Sparql2Daviz(base.ATCTContent):
    """Sparql2Daviz"""
    implements(ISparql2Daviz)

    meta_type = "Sparql2Daviz"
    schema = Sparql2DavizSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(Sparql2Daviz, PROJECTNAME)

def handle_object_initialized(obj, event):
    """Handle object initialized"""
    sparqldata = obj.aq_parent.execute_query()
    columns = getColumns(sparqldata)

    notify(DavizEnabledEvent(obj, columns=columns))
