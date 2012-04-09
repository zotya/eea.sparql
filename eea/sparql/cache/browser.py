""" Browser
"""
import hashlib
from zope import event
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from eea.sparql.cache import InvalidateCacheEvent, cacheSparqlKey

class InvalidateCache(BrowserView):
    """ Caching for sparql query results """

    def __call__(self):
        if not "submit" in self.request.form:
            return self.index()

        key = cacheSparqlKey(self.context.execute_query, self.context)
        key = 'eea.sparql.content.sparql.execute_query:%s' % key
        key = hashlib.md5(key).hexdigest()
        event.notify(InvalidateCacheEvent(key=key, raw=True))

        IStatusMessage(self.request).addStatusMessage("Cache invalidated")
        return self.index()
