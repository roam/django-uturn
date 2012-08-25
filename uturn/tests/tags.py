# -*- coding: utf-8 -*-
from django.test import TestCase
from django.template import Template, RequestContext
from django import VERSION as django_version

from .http import GET

if django_version[:2] in ((1, 2), (1, 3,), (1, 4)):
    NAME = 'with_params'
else:
    NAME = "'with_params'"


class DefaultUrlTemplateTagTest(TestCase):

    def test_plain(self):
        uturn = Template("{% load uturn %}{% defaulturl " + NAME + " 'hi' %}")
        url = Template("{% load uturn %}{% url " + NAME + " 'hi' %}")
        c = RequestContext(GET())
        self.assertEqual(url.render(c), uturn.render(c))

    def test_override(self):
        uturn = Template("{% load uturn %}{% defaulturl " + NAME + " 'hi' %}")
        url = Template("{% load uturn %}{% url " + NAME + " 'hi' %}")
        c = RequestContext(GET({'next': '/login'}))
        self.assertEqual('/login', uturn.render(c))
        self.assertEqual('/with-params/hi/', url.render(c))


class UturnTemplateTagTest(TestCase):

    def test_plain(self):
        uturn = Template("{% load uturn %}{% uturn " + NAME + " 'hi' %}")
        url = Template("{% load uturn %}{% url " + NAME + " 'hi' %}")
        c = RequestContext(GET())
        self.assertEqual(url.render(c), uturn.render(c))


    def test_override(self):
        uturn = Template("{% load uturn %}{% uturn " + NAME + " 'hi' %}")
        url = Template("{% load uturn %}{% url " + NAME + " 'hi' %}")
        c = RequestContext(GET({'next': '/login'}))
        self.assertEqual('/with-params/hi/?next=%2Flogin', uturn.render(c))
        self.assertEqual('/with-params/hi/', url.render(c))


class UturnParamTemplateTagTest(TestCase):

    def setUp(self):
        from django import VERSION
        super(UturnParamTemplateTagTest, self).setUp()
        self.with_request = VERSION[:2] == (1, 2)

    def test_plain(self):
        if self.with_request:
            uturn = Template("{% load uturn %}{% uturn_param request %}")
        else:
            uturn = Template("{% load uturn %}{% uturn_param %}")
        c = RequestContext(GET())
        self.assertEqual("", uturn.render(c))


    def test_override(self):
        if self.with_request:
            uturn = Template("{% load uturn %}{% uturn_param request %}")
        else:
            uturn = Template("{% load uturn %}{% uturn_param %}")
        c = RequestContext(GET({'next': '/okay-then'}))
        html = uturn.render(c)
        self.assertTrue(" value='/okay-then'" in html)
        self.assertTrue(" name='next'" in html)
