# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='django-uturn',
    version='0.3.1',
    author='Kevin Wetzels',
    author_email='kevin@roam.be',
    url='https://github.com/roam/django-uturn',
    install_requires=['Django>=1.4'],
    packages=['uturn', 'uturn.templatetags'],
    license='BSD',
    description='Overriding redirects in Django, to return where you came '\
                'from',
    long_description=open('README.rst').read(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
   ],
)
