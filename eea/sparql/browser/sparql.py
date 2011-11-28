from Products.Five import BrowserView
from Products.ZSPARQLMethod.Method import ZSPARQLMethod
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class SPARQL(BrowserView):
    template = ViewPageTemplateFile('test_query.pt')

    def __call__ (self):
        test_query = ZSPARQLMethod(self.context.id, self.context.title, self.context.endpoint)
        test_query.query = self.context.query()
        if self.context.timeout > 0:
            test_query.timeout = self.context.timeout
        test_query_results = test_query.__call__()
        test_query.arg_spec = self.context.arguments
        test_query.ZCacheable_invalidate()

        self.test_results = test_query()
        return self.template()