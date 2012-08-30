# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import template, VERSION as django_version
from django.template.defaulttags import URLNode
from django.utils.http import urlencode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from uturn.http import get_redirect_url, param_name


register = template.Library()


class DefaultUrlNode(URLNode):
    """
    Duplicate of the standard Django URL node that will render the "uturn"
    parameter from the request or if no such parameter exists, the URL supplied
    to the tag.

    It assumes the Context is a RequestContext. Make sure you've added the
    following template context processor in your settings as this provides
    access to the request from within the template tag::

        TEMPLATE_CONTEXT_PROCESSORS += (
            'django.core.context_processors.request',
        )

    An example. Usually you'd use the following to render a link::

        {% url viewname id %}

    If you want to give the optional ``uturn`` request parameter precedence
    over the normal url, you'd use this::

        {% defaulturl viewname id %}

    Now when you visit the page with the above template, you'll either have
    the same link that results from the normal url template tag, or, when a
    valid uturn parameter is present, a link to the value of the uturn
    parameter.
    """
    def __init__(self, url_node):
        self.url_node = url_node

    def render(self, context):
        next = get_redirect_url(context.get('request', None))
        url = next if next else self.url_node.render(context)
        if self.url_node.asvar:
            context[self.url_node.asvar] = url
            return ''
        return url


class UturnUrlNode(URLNode):
    """
    Duplicate of the standard Django URL node that will add the current request
    path to the URL.

    The page at the given link will then receive the ``next`` request
    parameter, which means you can redirect the user back to the page
    containing the uturn template tag, overriding the default redirect.

    It assumes the Context is a RequestContext. Make sure you've added the
    following template context processor in your settings as this provides
    access to the request from within the template tag::

        TEMPLATE_CONTEXT_PROCESSORS += (
            'django.core.context_processors.request',
        )

    An example. Usually you'd use the following to render a link::

        {% url viewname id %}

    Suppose that page contains a form and you want the user to be redirected
    to the current page rather than following the default redirect::

        {% uturn viewname id %}

    Of course, the view should use the Uturn redirect mechanisms for this to
    work. If you have a "Cancel" link on the form to take the user back to
    the previous page, use the ``defaulturl`` template tag::

        {% defaulturl previousviewname id %}
    """
    def __init__(self, url_node):
        self.url_node = url_node

    def render(self, context):
        url = self.url_node.render(context)
        request = context.get('request', None)
        if request:
            next = request.path
            param = param_name()
            part = urlencode({param: next})
            sep = '&' if url.find('?') >= 0 else '?'
            url = url + sep + part
        if self.url_node.asvar:
            context[self.url_node.asvar] = url
            return ''
        return url


@register.tag(name='defaulturl')
def do_default_url(parser, token):
    """
    Renders the supplied url or, in case a valid ``next`` parameter was
    passed, the value of the ``next`` parameter.

    This template tag behaves exactly like Django's default ``url`` tag when
    no ``next`` url was found in the request.

    """
    node = template.defaulttags.url(parser, token)
    return DefaultUrlNode(node)


@register.tag(name='uturn')
def do_uturn(parser, token):
    """
    Renders the supplied url while adding the current request path to the query
    string.

    This template tag behaves exactly like Django's default ``url`` tag. It
    just adds the current full request path to the url as the ``next``
    parameter.

    """
    node = template.defaulttags.url(parser, token)
    return UturnUrlNode(node)


def _do_uturn_param(request):
    next = get_redirect_url(request)
    if next:
        attr = {
            'param': conditional_escape(param_name()),
            'value': conditional_escape(next)
        }
        f = "<input type='hidden' name='%(param)s' value='%(value)s'>" % attr
        return mark_safe("<div style='display:none'>%s</div>" % f)
    return ''


# This is ugly stuff, but if this is all it takes to support Django 1.2, it'll
# have to do.
if django_version[:2] == (1, 2):
    @register.simple_tag
    def uturn_param(request):
        return _do_uturn_param(request)
else:
    @register.simple_tag(takes_context=True)
    def uturn_param(context):
        return _do_uturn_param(context.get('request', None))
