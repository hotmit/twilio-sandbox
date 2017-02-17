from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django import forms
from django.utils.translation import ugettext as _


class SendSmsForm(forms.Form):
    phone_number = forms.CharField(label=_('Phone Number'), required=True)
    message = forms.CharField(label=_('Message'), required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        h = FormHelper()
        h.form_method = 'POST'
        h.form_action = '/send-sms/'
        h.add_input(Submit('submit', _('Send')))

        self.helper = h