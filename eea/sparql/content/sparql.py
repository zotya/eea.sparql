"""Definition of the Sparql content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.Archetypes.atapi import StringField, StringWidget, \
                                    IntegerField, IntegerWidget, \
                                    TextField, TextAreaWidget

from Products.ZSPARQLMethod.Method import ZSPARQLMethod, \
                                        parse_arg_spec, map_arg_values

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.folder import ATBTreeFolder
from Products.Archetypes.atapi import Schema
from eea.sparql.interfaces import ISparql
from eea.sparql.config import PROJECTNAME


SparqlSchema = getattr(ATBTreeFolder, 'schema', Schema(())).copy() + \
            atapi.Schema((
    StringField(
        name='endpoint_url',
        widget=StringWidget(
            label="Sparql endpoint URL",
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
        name='arg_spec',
        widget=StringWidget(
            label="Arguments",
        ),
        required=0
    ),
    TextField(
        name='sparql_query',
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),

        widget=TextAreaWidget(
            label="Query",
        ),
        required=1
    ),


))

SparqlSchema['title'].storage = atapi.AnnotationStorage()
SparqlSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(SparqlSchema, moveDiscussion=False)


class Sparql(ATBTreeFolder, ZSPARQLMethod):
    """Sparql"""
    implements(ISparql)

    meta_type = "Sparql"
    schema = SparqlSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    security = ClassSecurityInfo()

    @property
    def query(self):
        """query"""
        return self.sparql_query()

    security.declarePublic("execute_query")
    def execute_query(self, args=None):
        """execute query"""
        arg_spec = parse_arg_spec(self.arg_spec)
        arg_values = map_arg_values(arg_spec, args)[1]
        return self.execute(**self.map_arguments(**arg_values))

atapi.registerType(Sparql, PROJECTNAME)
