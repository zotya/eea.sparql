from Products.Five import BrowserView
from Products.ZSPARQLMethod.Method import ZSPARQLMethod, parse_arg_spec, map_arg_values, interpolate_query_html
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from time import time

class SPARQL(BrowserView):

    def __init__(self, *args, **kwargs):
        BrowserView.__init__(self, *args, **kwargs)
        self.method = ZSPARQLMethod(self.context.id, self.context.title, self.context.endpoint)

    def execute(self, **arg_values):
        self.method = ZSPARQLMethod(self.context.id, self.context.title, self.context.endpoint)
        self.method.query = self.context.query()
        if self.context.timeout > 0:
            self.method.timeout = self.context.timeout
        self.method.arg_spec = self.context.arguments

        return self.method(**arg_values)

    _test_html = ViewPageTemplateFile('test_query.pt', globals())
    def test_query(self, REQUEST):
        """
        Execute the query and pretty-print the results as an HTML table.
        """

        self.method.arg_spec = self.context.arguments
        arg_spec = parse_arg_spec(self.method.arg_spec)
        missing, arg_values = map_arg_values(arg_spec, REQUEST.form)
        error = None

        if missing:
            # missing argument
            data = None
            dt = 0

        else:
            t0 = time()

            try:
                data = self.execute(**arg_values)

            except Exception, e:
                import traceback
                error = traceback.format_exc()
                data = None

            dt = time() - t0

        options = {
            'query': interpolate_query_html(self.method.query, arg_values),
            'data': data,
            'duration': dt,
            'arg_spec': arg_spec,
            'error': error,
        }
        return self._test_html(REQUEST, **options)


