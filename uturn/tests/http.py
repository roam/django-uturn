# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory

from ..http import get_redirect_url, smart_redirect, SmartHttpResponseRedirect


def GET(data=None):
    data = data if data else {}
    return RequestFactory().get('/path', data)


def POST(data=None):
    data = data if data else {}
    return RequestFactory().post('/path', data)


class GetRedirectUrlTest(TestCase):

    def tearDown(self):
        setattr(settings, 'UTURN_REDIRECT_PARAM', 'next')
        setattr(settings, 'UTURN_ALLOWED_HOSTS', None)
        super(GetRedirectUrlTest, self).tearDown()

    def test_none(self):
        self.assertTrue(get_redirect_url(GET()) is None)

    def test_none_param_changed(self):
        setattr(settings, 'UTURN_REDIRECT_PARAM', 'uturn')
        self.assertTrue(get_redirect_url(GET()) is None)

    def test_ok(self):
        request = GET({'next': '/nextone'})
        self.assertEqual('/nextone', get_redirect_url(request))

    def test_ok_param_changed(self):
        setattr(settings, 'UTURN_REDIRECT_PARAM', 'uturn')
        request = GET({'uturn': '/nextone'})
        self.assertEqual('/nextone', get_redirect_url(request))

    def test_relative_only(self):
        request = GET({'next': 'http://google.com'})
        self.assertTrue(get_redirect_url(request) is None)
        request = GET({'next': 'google.com'})
        self.assertTrue(get_redirect_url(request) is None)

    def test_whitelisted_domain(self):
        setattr(settings, 'UTURN_ALLOWED_HOSTS', ['google.com'])
        request = GET({'next': 'http://google.com'})
        self.assertEqual('http://google.com', get_redirect_url(request))
        # No prefix means google.com is interpreted as a path, not a domain
        request = GET({'next': 'google.com'})
        self.assertTrue(get_redirect_url(request) is None)
        # A protocol relative URL however, will have the domain compared
        # against our whitelist
        request = GET({'next': '//google.com'})
        self.assertEqual('//google.com', get_redirect_url(request))
        request = GET({'next': '//agoogle.com'})
        self.assertTrue(get_redirect_url(request) is None)
        request = GET({'next': 'http://agoogle.com'})
        self.assertTrue(get_redirect_url(request) is None)

    def test_relative_only_param_changed(self):
        setattr(settings, 'UTURN_REDIRECT_PARAM', 'uturn')
        request = GET({'uturn': 'http://google.com'})
        self.assertTrue(get_redirect_url(request) is None)
        request = GET({'uturn': 'google.com'})
        self.assertTrue(get_redirect_url(request) is None)

    def test_data_url(self):
        data_url = 'data:text/html,<script>window.alert("xss")</script>'
        request = GET({'next': data_url})
        self.assertTrue(get_redirect_url(request) is None)

    def test_file_url(self):
        request = GET({'next': 'file:///etc/passwd'})
        self.assertTrue(get_redirect_url(request) is None)

    def test_mailto_url(self):
        request = GET({'next': 'mailto:test@example.com'})
        self.assertTrue(get_redirect_url(request) is None)

    def test_mailto_url_whitelisted_domain(self):
        setattr(settings, 'UTURN_ALLOWED_HOSTS', ['example.com'])
        request = GET({'next': 'mailto:test@example.com'})
        self.assertTrue(get_redirect_url(request) is None)


class RedirectTestCase(TestCase):

    def tearDown(self):
        setattr(settings, 'UTURN_REDIRECT_PARAM', 'next')
        setattr(settings, 'UTURN_ALLOWED_HOSTS', None)
        super(RedirectTestCase, self).tearDown()

    def redirect(self, request, to):
        response = smart_redirect(request, to)
        return response['Location']

    def normal(self, method=GET):
        request = method()
        self.assertEqual('/default', self.redirect(request, '/default'))

    def normal_param_change(self, method=GET):
        setattr(settings, 'UTURN_REDIRECT_PARAM', 'uturn')
        self.normal(method)

    def override(self, param='next', method=GET):
        request = method({param: '/other'})
        self.assertEqual('/other', self.redirect(request, '/default'))

    def override_param_change(self, method=GET):
        setattr(settings, 'UTURN_REDIRECT_PARAM', 'uturn')
        self.override('uturn', method)

    def relative_only(self, param='next', method=GET):
        request = method({param: 'http://google.com'})
        self.assertEqual('/default', self.redirect(request, '/default'))
        request = method({param: 'google.com'})
        self.assertEqual('/default', self.redirect(request, '/default'))

    def relative_only_param_changed(self, method=GET):
        setattr(settings, 'UTURN_REDIRECT_PARAM', 'uturn')
        self.relative_only('uturn', method)

    def whitelisted_domain(self, method=GET):
        domains = ['google.com', 'twitter.com']
        setattr(settings, 'UTURN_ALLOWED_HOSTS', domains)
        for domain in domains:
            request = method({'next': 'http://' + domain})
            self.assertEqual('http://' + domain, get_redirect_url(request))
            # No prefix means the domain is interpreted as a path, not a domain
            request = method({'next': domain})
            self.assertTrue(get_redirect_url(request) is None)
            # A protocol relative URL however, will have the domain compared
            # against our whitelist
            request = method({'next': '//' + domain})
            self.assertEqual('//' + domain, get_redirect_url(request))
            request = method({'next': '//a' + domain})
            self.assertTrue(get_redirect_url(request) is None)
            request = method({'next': 'http://a' + domain})
            self.assertTrue(get_redirect_url(request) is None)


class SmartRedirectTest(RedirectTestCase):

    def test_normal(self):
        self.normal()

    def test_normal_post(self):
        self.normal(method=POST)

    def test_normal_param_change(self):
        self.normal_param_change()

    def test_normal_param_change_post(self):
        self.normal_param_change(method=POST)

    def test_override(self):
        self.override()

    def test_override_post(self):
        self.override(method=POST)

    def test_override_param_change(self):
        self.override_param_change()

    def test_override_param_change_post(self):
        self.override_param_change(method=POST)

    def test_relative_only(self):
        self.relative_only()

    def test_relative_only_post(self):
        self.relative_only(method=POST)

    def test_relative_only_param_changed(self):
        self.relative_only_param_changed()

    def test_relative_only_param_changed_post(self):
        self.relative_only_param_changed(method=POST)

    def test_whitelisted_domain(self):
        self.whitelisted_domain()

    def test_whitelisted_domain_post(self):
        self.whitelisted_domain(method=POST)


class SmartHttpResponseRedirectTest(RedirectTestCase):

    def redirect(self, request, to):
        response = SmartHttpResponseRedirect(request, to)
        return response['Location']

    def test_normal(self):
        self.normal()

    def test_normal_post(self):
        self.normal(method=POST)

    def test_normal_param_change(self):
        self.normal_param_change()

    def test_normal_param_change_post(self):
        self.normal_param_change(method=POST)

    def test_override(self):
        self.override()

    def test_override_post(self):
        self.override(method=POST)

    def test_override_param_change(self):
        self.override_param_change()

    def test_override_param_change_post(self):
        self.override_param_change(method=POST)

    def test_relative_only(self):
        self.relative_only()

    def test_relative_only_post(self):
        self.relative_only(method=POST)

    def test_relative_only_param_changed(self):
        self.relative_only_param_changed()

    def test_relative_only_param_changed_post(self):
        self.relative_only_param_changed(method=POST)

    def test_whitelisted_domain(self):
        self.whitelisted_domain()

    def test_whitelisted_domain_post(self):
        self.whitelisted_domain(method=POST)
