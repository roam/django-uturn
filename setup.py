# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django-uturn',
    version='0.2.4',
    author='Kevin Wetzels',
    author_email='kevin@roam.be',
    url='https://github.com/roam/django-uturn',
    packages=['uturn', 'uturn.templatetags'],
    license='BSD licence, see LICENCE',
    description='Overriding redirects in Django, to return where you came '\
                'from',
    long_description=open('README.rst').read(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
   ],
)