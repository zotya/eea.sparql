"""Definition of the SPARQL content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.Archetypes.atapi import StringField, StringWidget, IntegerField, IntegerWidget, TextField, TextAreaWidget

# -*- Message Factory Imported Here -*-

from eea.sparql.interfaces import ISPARQL
from eea.sparql.config import PROJECTNAME

SPARQLSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    StringField(
        name='endpoint',
        widget=StringWidget(
            label="SPARQL endpoint URL",
        ),
        required=1
    ),
    IntegerField(
        name='timeout',
        widget=IntegerWidget(
            label="Timeout",
        ),
        required=0
    ),
    StringField(
        name='arguments',
        widget=StringWidget(
            label="Arguments",
        ),
        required=0
    ),
    TextField(
        name='query',
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),

        widget=TextAreaWidget(
            label="Query",
        ),
        required=1
    ),


))

SPARQLSchema['title'].storage = atapi.AnnotationStorage()
SPARQLSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(SPARQLSchema, moveDiscussion=False)


class SPARQL(base.ATCTContent):
    """SPARQL"""
    implements(ISPARQL)

    meta_type = "SPARQL"
    schema = SPARQLSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


atapi.registerType(SPARQL, PROJECTNAME)
