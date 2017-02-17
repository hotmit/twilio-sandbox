from django.shortcuts import render
from twilio_sandbox.apps.twilio.forms import SendSmsForm


def view_twilio_sandbox(request):
    sms_form = SendSmsForm()
    context = {
        'sms_form': sms_form,
    }
    return render(request, 'twilio/home.html', context)


def view_send_sms(request):
    message = ''
    sms_form = SendSmsForm()

    if request.POST:
        sms_form = SendSmsForm(request.POST)
        if sms_form.is_valid():
            message = 'Sms sent!'

    context = {
        'message': message,
        'sms_form': sms_form,
    }
    return render(request, 'twilio/home.html', context)