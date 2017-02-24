from django.http import HttpResponse
from django.shortcuts import render
from twilio import twiml
from twilio_config import twilio_test
from twilio_sandbox.apps.twilio.forms import SendSmsVoiceForm


def view_twilio_sandbox(request):
    test_data = {
        'phone_number': twilio_test['default_phone_no'],
        'message': 'Hello from me!',
    }

    sms_form = SendSmsVoiceForm(initial=test_data)
    context = {
        'sms_form': sms_form,
    }
    return render(request, 'twilio/home.html', context)


def view_send_sms(request):
    display_message = ''
    sms_form = SendSmsVoiceForm()

    if request.POST:
        sms_form = SendSmsVoiceForm(request.POST)
        if sms_form.is_valid():
            display_message = 'Sms sent!'
            try:
                sms_form.send_sms()
            except Exception as ex:
                display_message = 'Error: %s' % ex

    context = {
        'message': display_message,
        'sms_form': sms_form,
    }
    return render(request, 'twilio/home.html', context)


def view_twilio_voice_answer(request):
    pass


def view_twilio_sms_answer(request):
    pass


def view_twilio_xml(request):
    message = request.GET.get('message', 'hello there! how are you today?')
    lang = request.GET.get('lang', 'en')
    voice = request.GET.get('voice', 'alice')

    r = twiml.Response()
    #language=lang,
    r.say(message, voice=voice)
    r.hangup()

    return HttpResponse(str(r), content_type='text/xml; charset=utf-8')

