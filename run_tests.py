# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management import call_command

def main():
    settings.configure(
        INSTALLED_APPS = (
            'django.contrib.contenttypes',
            'uturn',
        ),
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3'
            }
        },
        ROOT_URLCONF='uturn.tests.urls',
        TEMPLATE_CONTEXT_PROCESSORS = (
            'django.core.context_processors.request',
        ),
    )
    call_command('test', 'uturn')

if __name__ == '__main__':
    main()