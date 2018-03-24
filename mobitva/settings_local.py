from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mobitva',
        'PASSWORD': '12345',
        'USER': 'root',
        'PORT': '3306',
        'HOST': 'localhost'
    }
}