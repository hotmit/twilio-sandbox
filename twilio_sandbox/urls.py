from django.conf.urls import url
from twilio_sandbox.apps.request_recorder.views import view_record_request, view_records
from twilio_sandbox.apps.twilio import views as twilio_views


urlpatterns = [
    url(r'^$', twilio_views.view_twilio_sandbox, name='twilio_sandbox'),

    url(r'^outgoing-voice$', twilio_views.view_twilio_outgoing_voice, name='twilio_outgoing_voice'),
    url(r'^gather-input$', twilio_views.view_twilio_gather_input, name='twilio_gather_input'),
    url(r'^twilio/$', twilio_views.view_twilio_submit, name='twilio_submit'),

    url(r'^record/$', view_record_request, name='record_request'),
    url(r'^records/$', view_records, name='view_records'),
]
