from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django import forms
from django.utils.translation import ugettext as _

# /usr/bin/env python
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
from django.conf import settings
from twilio_config import twilio_config


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

    def send_sms(self):
        data = self.cleaned_data
        phone_number = data['phone_number']
        body = data['message']

        client = TwilioRestClient(twilio_config['account'], twilio_config['token'])
        sms_message = client.messages.create(to=phone_number, from_=twilio_config['phone_number'],
                                             body=body)

        print(sms_message)

