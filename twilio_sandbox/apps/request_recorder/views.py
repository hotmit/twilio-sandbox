from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from twilio_sandbox.apps.request_recorder.models import IncomingRequest


def view_record_request(request):
    IncomingRequest.record_message('Request Recorder', request)
    return HttpResponse('Thanks bud!')


def view_records(request):
    if request.GET.get('clear', None):
        IncomingRequest.objects.all().delete()
        return redirect(request.build_absolute_uri('?'))

    records = IncomingRequest.objects.all()

    context = {
        'records': records,
    }
    return render(request, 'request_recorder/index.html', context)