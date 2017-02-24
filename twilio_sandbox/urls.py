from django.conf.urls import url
from twilio_sandbox.apps.request_recorder.views import view_record_request, view_records
from twilio_sandbox.apps.twilio import views as twilio_views


urlpatterns = [
    url(r'^$', twilio_views.view_twilio_sandbox, name='twilio_sandbox'),
    url(r'^voice-ans$', twilio_views.view_twilio_voice_answer, name='twilio_voice_answer'),
    url(r'^sms-ans$', twilio_views.view_twilio_sms_answer, name='twilio_sms_answer'),
    url(r'^xml$', twilio_views.view_twilio_xml, name='twilio_xml'),
    url(r'^send/$', twilio_views.view_send_sms, name='send_sms'),

    url(r'^record/$', view_record_request, name='record_request'),
    url(r'^records/$', view_records, name='view_records'),
]
