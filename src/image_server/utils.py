# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import json
import hashlib
import requests
from django.conf import settings


def remove(path):
    n_path = path_on_filesystem(path)
    return os.remove(n_path)


def path_on_filesystem(path, mount_point=settings.FILE_STORAGE_PATH):
    digest = hashlib.sha1(path.encode('utf-8')).hexdigest()
    return os.path.join(mount_point,
                        str(digest[:2]),
                        str(digest[2:]))


def generate_thumbor_cached_link(image_url, **kwargs):
    data = {
        'image_url': image_url,
        'kwargs': kwargs
    }
    r = requests.get(settings.AVARSHA_SERVER, json=data)
    content = json.loads(r.content)
    return content['url']

