# -*- coding: utf-8 -*-
import urlparse

from django.shortcuts import redirect as core_redirect
from django.http import HttpResponseRedirect
from django.utils.encoding import iri_to_uri
from django.conf import settings


def param_name():
    return getattr(settings, 'UTURN_REDIRECT_PARAM', 'next')


def get_redirect_url(request):
    """
    Retrieves the next URL from the request.
    
    The next URL parameter is identified by the ``UTURN_REDIRECT_PARAM``, 
    which defaults to ``next``. If the parameter is present and is a
    relative URL, it will be returned. In any other case, ``None`` is 
    returned.

    Only URLs pointing to whitelisted domains (specified in the setting
    ``UTURN_ALLOWED_HOSTS``) and the current domain are allowed to prevent 
    redirects to untrusted sites. Have a look at 
    `URL Redirection to Untrusted site 
    <http://cwe.mitre.org/data/definitions/601.html>`_ to discover the risks
    involved.

    """
    if request is None:
        return None
    next = None
    param = param_name()
    if request.method == 'GET':
        next = request.GET.get(param, None)
    elif request.method == 'POST':
        next = request.POST.get(param, None)
    if not next:
        return None
    # Check if it's an absolute URL.
    allowed_hosts = getattr(settings, 'UTURN_ALLOWED_HOSTS', None)
    allowed_hosts = allowed_hosts if allowed_hosts else [request.get_host()]
    host = urlparse.urlparse(next)[1]
    if host:
        # Make sure the absolute URL points to an allowed host, otherwise 
        # ignore the value.
        return next if host in allowed_hosts else None
    # Make sure it's a relative URL to prevent "open redirects"
    return next if next.startswith('/') else None


def smart_redirect(request, to, *args, **kwargs):
    """
    Either redirects the user like Django's ``redirect`` shortcut would, or
    in case a redirect url is present, redirects to that instead.
    
    The next parameter takes precedence.

    """
    next = get_redirect_url(request)
    if next:
        return core_redirect(next)
    return core_redirect(to, *args, **kwargs)


def smart_response(request, response):
    """
    Reissues a redirect when necessary - leaves other response alone.

    The response is examined; in case it's a temporary redirect and a 
    redirect alternative is specified in the request, a new redirect is 
    constructed targeting the alternative. In all other cases, the response 
    is returned as is.

    """
    if not response:
        return response
    location = response.get('Location', None)
    if not location or response.status_code != 302:
        return response
    next = get_redirect_url(request)
    if next:
        response['Location'] = iri_to_uri(next)
    return response


class SmartHttpResponseRedirect(HttpResponseRedirect):
    """
    Acts like Django's regular ``HttpResponseRedirect``, unless a redirect
    alternative is discovered in the request parameters.
    
    """

    def __init__(self, request, redirect_to):
        next = get_redirect_url(request)
        redirect_to = next if next else redirect_to
        super(SmartHttpResponseRedirect, self).__init__(redirect_to)
