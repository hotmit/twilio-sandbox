from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from twilio_sandbox.apps.request_recorder.models import IncomingRequest


def view_record_request(request):
    req = IncomingRequest()
    req.set_message(request)
    req.save()
    return HttpResponse('Thanks bud!')


def view_records(request):
    records = IncomingRequest.objects.all()

    context = {
        'records': records,
    }
    return render(request, 'request_recorder/index.html', context)