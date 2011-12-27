""" Sparql interfaces module
"""

from zope.interface import Interface
from eea.daviz.interfaces import IExhibitJson
from eea.googlechartsconfig.interfaces import IGoogleChartJson

class ISparql(Interface):
    """ISparql"""

class ISparql2Daviz(IExhibitJson):
    """ISparql2Daviz"""

class ISparql2GoogleChart(IGoogleChartJson):
    """ISparql2GoogleChart"""
