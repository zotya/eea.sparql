""" Migrate sparqls with the new arguments format (name:type query)
"""

import logging
import datetime
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.app.async.interfaces import IAsyncService

logger = logging.getLogger("eea.sparql.upgrades")

def restart_sparqls(context):
    """ Migrate sparqls with the new arguments format (name:type query)
    """

    async = getUtility(IAsyncService)
    queues = async.getQueues()

    catalog = getToolByName(context, 'portal_catalog')
    pr = getToolByName(context, 'portal_repository')
    brains = catalog.searchResults(portal_type = 'Sparql')
    currentDate = datetime.datetime.now()
    needsRestart = []
    import pdb; pdb.set_trace()

    """ stop all sparql jobs """
    for queue in queues.values():
        jobs = [job for job in queue.__iter__()]
        for job in queue.__iter__():
            shouldRemove = False
            for arg in job.args:
                if hasattr(arg, 'func_name') and arg.func_name == 'async_updateLastWorkingResults':
                    shouldRemove = True
            if shouldRemove:
                queue.remove(job)
    import pdb; pdb.set_trace()
    for brain in brains:
        obj = brain.getObject()
        if obj.getRefresh_rate() != 'Once':
            needsRestart.append(obj)
#            try:
#                history = pr.getHistoryMetadata(obj)
#                retrieve = history.retrieve
#                lastChange = retrieve(history.getLength(countPurged = False) - 1,
#                                     countPurged=False)
#                lastModStamp = lastChange['metadata']['sys_metadata']['timestamp']
#                lastModDate = datetime.datetime.fromtimestamp(lastModStamp)
#                delta = currentDate - lastModDate
#                if delta.days > 14:
#                    possibleBroken.append(obj.absolute_url())
#                else:
#                    noProblemo.append(obj.absolute_url())
#            except:
#                .append(obj.absolute_url())
    import pdb; pdb.set_trace()