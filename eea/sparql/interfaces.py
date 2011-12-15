""" Sparql interfaces module
"""

from zope.interface import Interface
from eea.daviz.interfaces import IExhibitJson

class ISparql(Interface):
    """ISparql"""

class ISparql2Daviz(IExhibitJson):
    """ISparql2Daviz"""
