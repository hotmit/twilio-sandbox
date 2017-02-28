from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _


# Create your models here.
class IncomingRequest(models.Model):
    origin = models.TextField(verbose_name=_('origin'))
    message = models.TextField(verbose_name=_('message'))
    recorded_time = models.DateTimeField(auto_now_add=True, verbose_name=_('recorded time'))

    class Meta:
        db_table = 'tl_request'
        verbose_name = _('request')
        verbose_name_plural = _('requests')
        ordering = ('-recorded_time',)

    @classmethod
    def record_message(cls, origin, request):
        if request.GET or request.POST:
            get_var = dict(request.GET)
            post_var = dict(request.POST)

            context = {
                'GET': get_var,
                'POST': post_var,
            }

            message = render_to_string('request_recorder/message.html', context=context)
            req = IncomingRequest(origin=origin, message=message)
            req.save()

            return req
        return False
