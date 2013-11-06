# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponsePermanentRedirect

from .http import GET

from ..middleware import UturnMiddleware


def optional_redirect(request, redirect=None):
    if redirect:
        if redirect == '/permanent':
            return HttpResponsePermanentRedirect(redirect)
        return HttpResponseRedirect(redirect)
    return HttpResponse(b'hi')


class UturnMiddlewareTest(TestCase):

    def setUp(self):
        super(UturnMiddlewareTest, self).setUp()
        self.middleware = UturnMiddleware()

    def request(self, request, redirect=None):
        response = optional_redirect(GET(), redirect)
        return UturnMiddleware().process_response(request, response)

    def test_normal_response(self):
        response = self.request(GET())
        self.assertEqual(b'hi', response.content)

    def test_redirect_no_uturn(self):
        response = self.request(GET(), '/to-here')
        self.assertEqual('/to-here', response.get('Location', None))

    def test_redirect_uturn(self):
        response = self.request(GET({'next': '/no-here'}), '/to-here')
        self.assertEqual('/no-here', response.get('Location', None))

    def test_redirect_no_uturn_when_permanent(self):
        response = self.request(GET({'next': '/no-here'}), '/permanent')
        self.assertEqual('/permanent', response.get('Location', None))
