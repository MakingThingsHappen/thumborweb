from ..base import *

DEBUG = True
INSTALLED_APPS += ('debug_toolbar',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Test dir


CLOUDFLARE_EMAIL = 'chenzhigao@mingdabeta.com'
CLOUDFLARE_API_KEY = '5429536daa4802c477d8affe1b6ff0a8d7e1a'
CLOUDFLARE_ZONE = 'avarsha.com'
FILE_STORAGE_PATH = os.path.join(PROJ_DIR, 'image_server', 'tests')
AVARSHA_SERVER = 'http://192.168.1.120:8000/tools/get_thumbor_url/'
