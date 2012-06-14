# -*- coding: utf-8 -*-
from http import smart_response


class UturnMiddleware(object):
    """
    Middleware that applies the logic of the ``uturn`` decorator to each 
    request.

    If you want to enable Uturn redirects on each request, add this middleware
    class to your Django settings. If you prefer to explicitly specify which
    views can use uturn redirects, use the ``uturn.views.uturn`` decorator.
    
    """
    def process_response(self, request, response):
        return smart_response(request, response)
