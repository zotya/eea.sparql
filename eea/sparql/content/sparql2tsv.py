"""Definition of the SPARQL2TSV content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.Archetypes.atapi import StringField, StringWidget, IntegerField, IntegerWidget, TextField, TextAreaWidget


from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content import base
from Products.Archetypes.atapi import Schema
from eea.sparql.interfaces import ISPARQL2TSV
from eea.sparql.config import PROJECTNAME

SPARQL2TSVSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    StringField(
        name='X',
        widget=StringWidget(
            label="X",
        ),
        required=1
    ),

))

SPARQL2TSVSchema['title'].storage = atapi.AnnotationStorage()
SPARQL2TSVSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(SPARQL2TSVSchema, moveDiscussion=False)

class FakeTSV(object):
    """Fake TSV file"""

class SPARQL2TSV(base.ATCTContent):
    """SPARQL2TSV"""
    implements(ISPARQL2TSV)

    meta_type = "SPARQL2TSV"
    schema = SPARQL2TSVSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    security = ClassSecurityInfo()
    def getFile(self):
        import pdb; pdb.set_trace()
#        f = open('/home/zotya/Desktop/f1.tsv', 'r')
#        data = f.read()
        sparqldata = self.aq_parent.execute_query()
        tsvrows = []
        titles = "\t".join(sparqldata['var_names'])
        tsvrows.append(titles)
        for row in sparqldata['rows']:
            values = []
            for value in row:
                if value:
                    values.append(value.n3())
                else:
                    values.append('None')
            tsvrow = "\t".join(values)
            tsvrows.append(tsvrow)
        data = "\n".join(tsvrows)
        xx = FakeTSV()
        xx.data = data
        return xx
        
atapi.registerType(SPARQL2TSV, PROJECTNAME)
