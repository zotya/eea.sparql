from Products.Five import BrowserView
from Products.ZSPARQLMethod.Method import ZSPARQLMethod, parse_arg_spec, map_arg_values, interpolate_query_html
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from time import time

class SPARQL(BrowserView):

    def test_query(self):
        arg_spec = parse_arg_spec(self.context.arg_spec)
        missing, arg_values = map_arg_values(arg_spec, self.request.form)
        error = None

        if missing:
            # missing argument
            data = None
            dt = 0

        else:
            t0 = time()

            try:
                data = self.context.execute(**arg_values)

            except Exception, e:
                import traceback
                error = traceback.format_exc()
                data = None

            dt = time() - t0

        options = {
            'query': interpolate_query_html(self.context.query, arg_values),
            'data': data,
            'duration': dt,
            'arg_spec': arg_spec,
            'error': error,
        }

        return options
