from urllib import parse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.urls import reverse
from django.utils.translation import ugettext as _
from twilio.rest import Client
from twilio_config import twilio_config

# /usr/bin/env python
# Download the twilio-python library from http://twilio.com/docs/libraries


LANG_CHOICES = (('en', _('English')), ('fr', _('Français')))
VOICE_CHOICES = (('man', _('Man')), ('woman', _('Woman')), ('alice', _('Alice')))
TYPE_CHOICES = (('sms', _('SMS')), ('voice', _('Voice')))


class SendSmsVoiceForm(forms.Form):
    phone_number = forms.CharField(label=_('Phone Number'), required=True)
    type = forms.ChoiceField(label=_('Type'), required=True, choices=TYPE_CHOICES,
                             widget=forms.RadioSelect, initial='voice')
    language = forms.ChoiceField(label=_('Language'), required=True, choices=LANG_CHOICES,
                             widget=forms.RadioSelect, initial='en')
    voice = forms.ChoiceField(label=_('Voice'), required=True, choices=VOICE_CHOICES,
                             widget=forms.RadioSelect, initial='alice')
    message = forms.CharField(label=_('Message'), required=True, widget=forms.Textarea)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

        h = FormHelper()
        h.form_method = 'POST'
        h.form_action = reverse('twilio_submit')
        h.add_input(Submit('submit', _('Send')))
        self.helper = h

    def submit(self):
        data = self.cleaned_data
        phone_number = data['phone_number']
        message_type = data['type']
        text = data['message']
        from_number = twilio_config['phone_number']

        client = Client(twilio_config['account'], twilio_config['token'])

        if message_type == 'sms':
            sms_result = client.messages.create(to=phone_number, from_=from_number, body=text)
            return 'Sms sent!'
        else:
            url_param = {
                'message': text,
                'lang': data['language'],
                'voice': data['voice'],
            }
            url = '{url}/?{params}'.format(
                url=self.request.build_absolute_uri(reverse('twilio_outgoing_voice')),
                params=parse.urlencode(url_param)
            )
            voice_result = client.calls.create(to=phone_number, from_=from_number, url=url, timeout=30)
            return 'Voice sent!'


