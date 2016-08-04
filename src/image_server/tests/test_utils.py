# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
from django.test import TestCase
from image_server import utils


class UtilsTestCase(TestCase):
    def test_path_on_filesystem(self):
        path = 'logos/macys.png'
        mount_point = '/data/avarsha/images'
        expected = os.path.join(mount_point,
                                '6d/4aae71e43b2e56e028b2e86c1cb83d83758709')
        actually = utils.path_on_filesystem(path, mount_point)
        self.assertEqual(actually, expected)

    def test_generate_thumbor_cached_link(self):
        image_url = u'logos/macys.png'
        kwargs = {'width': 0, 'Smart': True, 'height': 100}
        expected = 'http://www.avarshacdn.com/rMqJKi20mGlY3E2vCyNUupjkU-0=/0x100/logos/macys.png'
        actually = utils.generate_thumbor_cached_link(image_url, **kwargs)
        self.assertEqual(expected, actually)
