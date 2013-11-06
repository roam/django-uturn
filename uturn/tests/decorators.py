# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponsePermanentRedirect
from django.views.generic import View

from .http import GET

from ..decorators import uturn


def view_definition(request, redirect=None):
    if redirect:
        if redirect == '/permanent':
            return HttpResponsePermanentRedirect(redirect)
        return HttpResponseRedirect(redirect)
    return HttpResponse(b'hi')


@uturn
def optional_redirect(request, redirect=None):
    return view_definition(request, redirect)


class OptionalRedirect(View):

    def dispatch(self, request, *args, **kwargs):
        return view_definition(request, kwargs.get('redirect'))


cbv_optional_redirect = uturn(OptionalRedirect.as_view())


class UturnDecoratorTest(TestCase):

    def test_normal_response(self):
        response = optional_redirect(GET())
        self.assertEqual(b'hi', response.content)

    def test_normal_response_cbv(self):
        response = cbv_optional_redirect(GET())
        self.assertEqual(b'hi', response.content)

    def test_redirect_no_uturn(self):
        response = optional_redirect(GET(), '/to-here')
        self.assertEqual('/to-here', response.get('Location', None))

    def test_redirect_no_uturn_cbv(self):
        response = cbv_optional_redirect(GET(), redirect='/to-here')
        self.assertEqual('/to-here', response.get('Location', None))

    def test_redirect_uturn(self):
        response = optional_redirect(GET({'next': '/no-here'}), '/to-here')
        self.assertEqual('/no-here', response.get('Location', None))

    def test_redirect_uturn_cbv(self):
        response = cbv_optional_redirect(GET({'next': '/no-here'}), redirect='/to-here')
        self.assertEqual('/no-here', response.get('Location', None))

    def test_redirect_no_uturn_when_permanent(self):
        response = optional_redirect(GET({'next': '/no-here'}), redirect='/permanent')
        self.assertEqual('/permanent', response.get('Location', None))

    def test_redirect_no_uturn_when_permanent_cbv(self):
        response = cbv_optional_redirect(GET({'next': '/no-here'}), redirect='/permanent')
        self.assertEqual('/permanent', response.get('Location', None))
