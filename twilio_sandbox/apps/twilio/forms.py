from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django import forms
from django.utils.translation import ugettext as _

# /usr/bin/env python
# Download the twilio-python library from http://twilio.com/docs/libraries
from django.conf import settings
from twilio.rest import Client
from twilio_config import twilio_config


class SendSmsVoiceForm(forms.Form):
    phone_number = forms.CharField(label=_('Phone Number'), required=True)
    type = forms.ChoiceField(label=_('Type'), required=True, choices=(('sms', _('SMS')), ('voice', _('Voice'))),
                             widget=forms.RadioSelect, initial='sms')
    language = forms.ChoiceField(label=_('Language'), required=True, choices=(('en', _('English')), ('fr', _('Français'))),
                             widget=forms.RadioSelect, initial='en')

    message = forms.CharField(label=_('Message'), required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        h = FormHelper()
        h.form_method = 'POST'
        h.form_action = '/send/'
        h.add_input(Submit('submit', _('Send')))

        self.helper = h

    def send_sms(self):
        data = self.cleaned_data
        phone_number = data['phone_number']
        message_type = data['type']
        body = data['message']
        from_number = twilio_config['phone_number']

        client = Client(twilio_config['account'], twilio_config['token'])

        if message_type == 'sms':
            sms_message = client.messages.create(to=phone_number, from_=from_number,
                                                 body=body)
        else:
            url = 'http://twilio.wadep.com/xml/'
            client.calls.create(to=phone_number, from_=from_number, url=url)


