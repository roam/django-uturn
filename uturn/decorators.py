# -*- coding: utf-8 -*-
from functools import wraps
from http import smart_response


def uturn(view):
    """
    Decorator for view functions that applies smart redirects when needed.

    If the view responds with a redirect, this decorator will check whether
    a *better* redirect location is specified in the request and if there is,
    override the redirect with the new location.

    This only applies to temporary redirects, not permanent redirects or any
    other kind of response.

    """
    @wraps(view)
    def wrap(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        return smart_response(request, response)
    return wrap
