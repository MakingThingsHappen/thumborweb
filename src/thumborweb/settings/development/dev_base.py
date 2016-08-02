from ..base import *


DEBUG = True
INSTALLED_APPS += ('debug_toolbar', )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Test dir
TEST_PATH = os.path.join(PROJ_DIR, 'image_server', 'tests')
