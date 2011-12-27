""" GoogleChart properties for sparql
"""

from eea.googlechartsconfig.browser.app import properties

class EditForm(properties.EditForm):
    """ Layer to edit googlechart properties for sparql data.
    """

    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('json')

