# -*- coding: utf-8 -*-
from django.test import TestCase
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponsePermanentRedirect

from http import GET

from ..decorators import uturn


@uturn
def optional_redirect(request, redirect=None):
    if redirect:
        if redirect == '/permanent':
            return HttpResponsePermanentRedirect(redirect)
        return HttpResponseRedirect(redirect)
    return HttpResponse('hi')


class UturnDecoratorTest(TestCase):

    def test_normal_response(self):
        response = optional_redirect(GET())
        self.assertEqual('hi', response.content)

    def test_redirect_no_uturn(self):
        response = optional_redirect(GET(), '/to-here')
        self.assertEqual('/to-here', response.get('Location', None))

    def test_redirect_uturn(self):
        response = optional_redirect(GET({'next': '/no-here'}), '/to-here')
        self.assertEqual('/no-here', response.get('Location', None))

    def test_redirect_no_uturn_when_permanent(self):
        response = optional_redirect(GET({'next': '/no-here'}), '/permanent')
        self.assertEqual('/permanent', response.get('Location', None))
