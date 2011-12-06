from eea.daviz.browser.app import properties
class EditForm(properties.EditForm):

    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('json')
        self.form_fields = self.form_fields.omit('sources')

