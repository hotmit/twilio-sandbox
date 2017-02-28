from urllib import parse
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from twilio import twiml
from twilio_config import twilio_test
from twilio_sandbox.apps.request_recorder.models import IncomingRequest
from twilio_sandbox.apps.twilio.forms import SendSmsVoiceForm


def view_twilio_sandbox(request):
    test_data = {
        'phone_number': twilio_test['default_phone_no'],
        'message': 'Sensor Point Six_B5228098_1, went out of range on 2017-02-16 9:50am eastern, in cooler, at Vaughan '
                   'valley. with alarm escalation level 1. the current Reading is 20.9°C. '
                   'Please press 1 to confirm this call.',
    }

    sms_form = SendSmsVoiceForm(request, initial=test_data)
    context = {
        'sms_form': sms_form,
    }
    return render(request, 'twilio/home.html', context)


def view_twilio_submit(request):
    display_message = ''
    sms_form = SendSmsVoiceForm(request)

    if request.POST:
        sms_form = SendSmsVoiceForm(request, data=request.POST)
        if sms_form.is_valid():
            try:
                display_message = sms_form.submit()
            except Exception as ex:
                display_message = 'Error: %s' % ex
                raise

    context = {
        'message': display_message,
        'sms_form': sms_form,
    }
    return render(request, 'twilio/home.html', context)


@csrf_exempt
def view_twilio_outgoing_voice(request):
    message = request.GET.get('message', 'hello there! how are you today?')
    lang = request.GET.get('lang', 'en')
    voice = request.GET.get('voice', 'alice')

    IncomingRequest.record_message('Twilio XML', request)

    r = twiml.Response()
    message = parse.unquote_plus(message)
    r.say(message, language=lang, voice=voice)

    gather_url = '{url}/?{params}'.format(
        url=request.build_absolute_uri(reverse(view_twilio_gather_input)),
        params=parse.urlencode(dict(request.GET))
    )
    r.gather(action=gather_url, timeout=10, numDigits=1)

    return HttpResponse(str(r), content_type='text/xml; charset=utf-8')


@csrf_exempt
def view_twilio_gather_input(request):
    lang = request.GET.get('lang', 'en')
    voice = request.GET.get('voice', 'alice')

    IncomingRequest.record_message('Twilio XML', request)

    r = twiml.Response()
    message = 'Thank you and goodbye!'
    r.say(message, language=lang, voice=voice)
    r.hangup()

    return HttpResponse(str(r), content_type='text/xml; charset=utf-8')
