""" sparql
"""

from Products.Five import BrowserView
from Products.ZSPARQLMethod.Method import interpolate_query_html
from Products.ZSPARQLMethod.Method import map_arg_values
from Products.ZSPARQLMethod.Method import parse_arg_spec
from eea.sparql.converter.sparql2json import sparql2json
from time import time
import json


class Sparql(BrowserView):
    """Sparql view"""

    def test_query(self):
        """test query"""
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

            except Exception:
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

    def json(self):
        """json"""
        data = self.context.execute_query()
        return json.dumps(sparql2json(data))


class Caching(BrowserView):

    def cache_managers(self):
        return self.context.ZCacheable_getManagerIds()

    def enabled(self):
        return self.context.ZCacheable_enabled()

    def current_manager(self):
        return self.context.ZCacheable_getManagerId()

    def __call__(self):
        if not "submit" in self.request.form:
            return self.index()

        manager_id = self.request.form.get("manager_id","")
        old_manager_id = self.context.ZCacheable_getManagerId()

        if manager_id != old_manager_id:
            self.context.ZCacheable_setManagerId(manager_id)

        enabled = self.request.form.get("enabled")

        if self.context.ZCacheable_enabled() != enabled:
            self.context.ZCacheable_setEnabled(bool(enabled))

        return self.index()


