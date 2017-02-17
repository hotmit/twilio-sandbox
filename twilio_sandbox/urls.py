from django.conf.urls import patterns, include, url
from django.contrib import admin
from twilio_sandbox.apps.request_recorder.views import view_record_request, view_records
from twilio_sandbox.apps.twilio.views import view_twilio_sandbox, view_send_sms

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twilio_sandbox.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^$', view_twilio_sandbox, name='twilio_sandbox'),
    url(r'^send-sms/$', view_send_sms, name='send_sms'),

    url(r'^record/$', view_record_request, name='record_request'),
    url(r'^records/$', view_records, name='view_records'),
    url(r'^admin/', include(admin.site.urls)),
)
