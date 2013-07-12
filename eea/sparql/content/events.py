""" Handle events
"""
import DateTime
from zope.component import getUtility
from plone.app.async.interfaces import IAsyncService
from eea.sparql.content.sparql import async_updateLastWorkingResults

def bookmarksfolder_added(obj, evt):
    """On new bookmark folder automatically fetch all queries"""
    obj.syncQueries()

def sparql_added_or_modified(obj, evt):
    """Update last working results when sparql is added or modified"""
    async = getUtility(IAsyncService)

    obj.scheduled_at = DateTime.DateTime()
    async.queueJob(async_updateLastWorkingResults,
                    obj,
                    scheduled_at = obj.scheduled_at)


