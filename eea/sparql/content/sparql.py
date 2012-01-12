"""Definition of the Sparql content type
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content import schemata, base
from Products.Archetypes import atapi
from Products.Archetypes.atapi import IntegerField, IntegerWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import StringField, StringWidget
from Products.Archetypes.atapi import TextField, TextAreaWidget
from Products.ZSPARQLMethod.Method import ZSPARQLMethod
from Products.ZSPARQLMethod.Method import parse_arg_spec, map_arg_values
from eea.cache import cache
from eea.sparql.config import PROJECTNAME
from eea.sparql.interfaces import ISparql
from zope.interface import implements


SparqlSchema = getattr(base.ATCTContent, 'schema', Schema(())).copy() + \
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

def cacheKeySparql(fun, self):
    """ Cache key for Sparql Query """
    return str(self.getArg_spec()) + str(self.getSparql_query())


class Sparql(base.ATCTContent, ZSPARQLMethod):
    """Sparql"""
    implements(ISparql)

    meta_type = "Sparql"
    schema = SparqlSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    security = ClassSecurityInfo()

    security.declarePublic('index_html')
    def index_html(self, REQUEST=None, **kwargs):
        """index_html"""
        return self.REQUEST.response.redirect(self.absolute_url()+"/@@view")

    @property
    def query(self):
        """query"""
        return self.sparql_query()

    security.declarePublic("execute_query")
    @cache(get_key=cacheKeySparql)
    def execute_query(self, args=None):
        """execute query"""
        arg_spec = parse_arg_spec(self.arg_spec)
        arg_values = map_arg_values(arg_spec, args)[1]
        return self.execute(**self.map_arguments(**arg_values))

atapi.registerType(Sparql, PROJECTNAME)
