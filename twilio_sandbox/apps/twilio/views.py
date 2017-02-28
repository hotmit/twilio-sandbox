from urllib import parse
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from twilio import twiml
from twilio.security import RequestValidator
from twilio_config import twilio_test, twilio_config
from twilio_sandbox.apps.request_recorder.models import IncomingRequest
from twilio_sandbox.apps.twilio.forms import SendSmsVoiceForm


def view_twilio_sandbox(request):
    test_data = {
        'phone_number': twilio_test['default_phone_no'],
        'message': 'Sensor Point Six_B5228098_1, went out of range on 2017-02-16 9:50am eastern, in cooler, at Vaughan '
                   'valley. with alarm escalation level 1. the current Reading is 20.9°C. '
                   'Please press 1 to acknowledge, press 7 to repeat this message.',
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


def twilio_callback(function):
    def _wrapper(request, *args, **kwargs):

        validator = RequestValidator(twilio_config['token'])
        signature = request.META.get('HTTP_X_TWILIO_SIGNATURE', '')
        is_valid = validator.validate(request.build_absolute_uri(), request.POST.dict(), signature)

        if is_valid:
            return function(request, *args, **kwargs)

        r = twiml.Response()
        r.reject('Invalid signature.')
        return HttpResponse(str(r), content_type='text/xml; charset=utf-8')

    return _wrapper


@csrf_exempt
@twilio_callback
def view_twilio_outgoing_voice(request):
    message = request.GET.get('message', '')
    lang = request.GET.get('lang', 'en')
    voice = request.GET.get('voice', 'alice')

    IncomingRequest.record_message('Outgoing', request)
    r = twiml.Response()

    if not message:
        r.reject('No message.')
    else:
        # r.pause(length=1)
        gather_url = '{url}/?{params}'.format(
            url=request.build_absolute_uri(reverse(view_twilio_gather_input)),
            params=parse.urlencode(request.GET.dict())
        )
        with r.gather(action=gather_url, timeout=10, numDigits=1) as g:
            message = parse.unquote_plus(message)
            g.say(message, language=lang, voice=voice)

    return HttpResponse(str(r), content_type='text/xml; charset=utf-8')


@csrf_exempt
@twilio_callback
def view_twilio_gather_input(request):
    pref = {
        'language': request.GET.get('lang', 'en'),
        'voice': request.GET.get('voice', 'alice'),
    }

    IncomingRequest.record_message('Gather', request)
    digit = int(request.POST.get('Digits', -10))
    r = twiml.Response()

    if digit == 7:
        url = '{url}/?{params}'.format(url=request.build_absolute_uri(reverse(view_twilio_outgoing_voice)),
                                       params=parse.urlencode(request.GET.dict()))
        r.redirect(url)
    elif digit == 1:
        message = 'Thank you and goodbye!'
        r.say(message, **pref)
        r.hangup()
    else:
        with r.gather(action=request.build_absolute_uri(), timeout=10, numDigits=1) as g:
            g.say('Please press 1 to acknowledge, press 7 to repeat this message.', **pref)

    return HttpResponse(str(r), content_type='text/xml; charset=utf-8')
