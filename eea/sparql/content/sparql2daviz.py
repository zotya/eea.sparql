"""Definition of the Sparql2Daviz content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.Archetypes.atapi import StringField, StringWidget, IntegerField, IntegerWidget, TextField, TextAreaWidget


from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content import base
from Products.Archetypes.atapi import Schema

from eea.sparql.interfaces import ISparql2Daviz
from eea.sparql.config import PROJECTNAME
from eea.sparql.converter.sparql2daviz import column_type

from zope.component import queryAdapter, queryUtility
from eea.daviz.converter.interfaces import IExhibitJsonConverter
from eea.daviz.interfaces import IDavizConfig
from eea.daviz.events import DavizEnabledEvent
from zope.event import notify

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
    sparqldata = obj.aq_parent.execute_query()
    columns = (column_type(col) for col in sparqldata['var_names'])

    notify(DavizEnabledEvent(obj, columns=columns))
