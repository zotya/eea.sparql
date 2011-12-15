""" Base module for sparql tests
"""

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

import eea.sparql

@onsetup
def setup_sparql():
    """Set up the additional products.
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', eea.sparql)
    fiveconfigure.debug_mode = False

    ztc.installPackage('eea.sparql')

setup_sparql()
ptc.setupPloneSite(products=['eea.sparql'])


class SparqlFunctionalTestCase(ptc.FunctionalTestCase):
    """ Base class for functional integration tests for the Sparql product.
    """
    def afterSetUp(self):
        """ After setup """
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])
