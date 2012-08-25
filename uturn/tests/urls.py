# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url


def default_view(request):
    return None


def other_view(request):
    return None

def with_params(request, *args, **kwargs):
    return None


urlpatterns = patterns('',
    url(r'^default/$', default_view, name='default_view'),
    url(r'^other/$', other_view, name='other_view'),
    url(r'^with-params/(?P<name>\w+)/$', with_params, name='with_params'),
)
