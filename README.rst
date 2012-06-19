============
django-uturn
============

Provides the HTTP redirect flexibility of Django's ``login`` view to the rest 
of your views.

Here's what happens when you --as an anonymous user-- try to access a view 
requiring you to log in:

1. Django redirects you to ``/login?next=/page-you-wanted-to-see``
2. You log on
3. Django's ``login`` view notices the ``next`` parameter and redirects you to
   ``/page-you-wanted-to-see`` rather than ``/``.

With Uturn, you'll be able to use the same feature by simply changing some
template code and adding middleware or decorators to your views.

----

Installation
------------
django-uturn is available on Pypi::

    pip install django-uturn

Uturn is currently tested against Django versions 1.2, 1.3 and 1.4.

.. image:: https://secure.travis-ci.org/roam/django-uturn.png?branch=master


----

Typical use cases
-----------------

From master to detail and back again
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You've got a list of... let's say *fish*. All kinds of fish. To enable users to
find fish by species, you've added a filter. Enter ``bass`` and your list is
trimmed to only contain the Australian Bass, Black Sea Bass, Giant Sea Bass, 
Bumble Bass...

Wait a minute! *Bumble Bass* isn't a species you've ever heard of - it's 
probably the European Bass. So you hit the edit link of the Bumble Bass, 
change the name and save the form. Your view redirects you to the list. The 
unfiltered list. *Aaargh!*

If you'd just used the Uturn redirect tools, you would have been redirected to
the filtered list. Much better (in most cases).


Multiple origins
^^^^^^^^^^^^^^^^

This is basically a more general application of the previous use case. Suppose
you have a form to create a new ticket that you can reach from both the project 
page and the ticket list page. When the user adds a new ticket, you want to 
make sure she's redirected to the project page when she came from the project 
page and the ticket list page when she reached the form from the ticket list 
page.

Enter Uturn.


How to use Uturn
----------------

Redirecting in views
^^^^^^^^^^^^^^^^^^^^

A typical form processing view function probably looks a bit like this::

    from django.shortcuts import redirect, render
    from forms import TicketForm

    def add_ticket(request):
        if request.method == 'POST':
            form = TicketForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('ticket-list')
        else:
            form = TicketForm()
        context = {'form': form}
        return render(request, 'tickets/ticket_list.html', context)

This view always redirects to the ticket list page. Add Uturn redirects::

    from django.shortcuts import render
    from uturn.decorators import uturn
    from forms import TicketForm

    @uturn
    def add_ticket(request):
        if request.method == 'POST':
            form = TicketForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('ticket-list')
        else:
            form = TicketForm()
        context = {'form': form}
        return render(request, 'tickets/ticket_list.html', context)

We simply add the ``uturn`` decorator to the view which will check the request 
for a valid ``next`` parameter and - if present - use that value as the 
target url for the redirect *instead* of the one you specified.

If you want to apply Uturn's redirect logic to *all* requests, add the 
``uturn.middleware.UturnMiddleware`` class to your middleware instead.


Passing the *next* page along
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

How do you add that ``next`` parameter to the URL in your project page? 
Here's what you'd normally use::

    <a href="{% url ticket-add %}">Add ticket</a>

This would render, depending on your url conf of course, a bit like this::

    <a href="/tickets/add/">Add ticket</a>

Here's what you'd use with Uturn::

    {% load uturn %}
    <a href="{% uturn ticket-add %}">Add ticket</a>

The ``uturn`` template tag will first determine the actual URL you want to link
to, exactly like the default ``url`` template tag would. But the ``uturn`` tag
will also add the *current* request path as the value for the ``next`` 
parameter::

    <a href="/tickets/add/?next=%2Fprojects%2F">Add ticket</a>

Clicking this link on the project page and adding a ticket will get you 
redirected to the ``/projects/`` URL *if you add the correct field to your
form*. 


Passing through forms
^^^^^^^^^^^^^^^^^^^^^

The easy way to add the parameter to your forms is by adding the 
``uturn_param`` template tag inside your form tags. If you're using
Django's builtin CSRF protection, you'll already have something like this::

    <form action="." method="post">
        {{ form.as_p }}
        {% csrf_token %}
        <input type="submit" value="Save">
    </form>

Change that to this::

    <form action="." method="post">
        {{ form.as_p }}
        {% csrf_token %}
        {% uturn_param %}
        <input type="submit" value="Save">
    </form>

**Note:** if you're using **Django 1.2**, you will have to pass the request::

    <form action="." method="post">
        {{ form.as_p }}
        {% csrf_token %}
        {% uturn_param request %}
        <input type="submit" value="Save">
    </form>

Don't worry if you *don't* want to use ``next`` as the parameter. You can 
specify a custom parameter name with the ``UTURN_REDIRECT_PARAM`` setting. And
if you want to redirect to other domains, you can specify those domains with
the ``UTURN_ALLOWED_HOSTS`` setting. Otherwise requests to redirect to other
domains will be ignored.


Overriding URLs in templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There's just one more thing we need to change: the *cancel* link on your form::

    <form action="." method="post">
        {{ form.as_p }}
        {% csrf_token %}{% uturn_param %}
        <input type="submit" value="Save"> or 
        <a href="{% url ticket-list %}">cancel</a>
    </form>

That link should point to the project page when applicable. Use the 
``defaulturl`` tag to accomplish this::

    {% load uturn %}
    <form action="." method="post">
        {{ form.as_p }}
        {% csrf_token %}{% uturn_param %}
        <input type="submit" value="Save"> or 
        <a href="{% defaulturl ticket-list %}">cancel</a>
    </form>

The ``defaulturl`` tag will default to standard ``url`` tag behavior and use
the ``next`` value when available. Here's what your form would look like from 
the ticket list page (with or without the ``next`` parameter)::

    <form action="." method="post">
        ...
        <input type="submit" value="Save"> or 
        <a href="/tickets/">cancel</a>
    </form>

And here's what that same form would look like when you reached it from the 
project page::

    <form action="." method="post">
        ...
        <input type="submit" value="Save"> or 
        <a href="/projects/">cancel</a>
    </form>


----

Thanks to `django-cms <https://github.com/divio/django-cms/>`_ for the 
backported implementation of ``RequestFactory``.
