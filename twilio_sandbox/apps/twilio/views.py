from django.shortcuts import render
from twilio_config import twilio_test
from twilio_sandbox.apps.twilio.forms import SendSmsForm


def view_twilio_sandbox(request):
    test_data = {
        'phone_number': twilio_test['default_phone_no'],
        'message': 'Hello from me!',
    }

    sms_form = SendSmsForm(initial=test_data)
    context = {
        'sms_form': sms_form,
    }
    return render(request, 'twilio/home.html', context)


def view_send_sms(request):
    display_message = ''
    sms_form = SendSmsForm()

    if request.POST:
        sms_form = SendSmsForm(request.POST)
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