""" Exhibit properties for sparql
"""

from eea.daviz.browser.app import properties

class EditForm(properties.EditForm):
    """ Layer to edit daviz properties for sparql data.
    """

    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('json')
        self.form_fields = self.form_fields.omit('sources')

