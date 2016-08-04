# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.conf.urls import include, url
from django.contrib import admin
from image_server.views import list_cwd_file

urlpatterns = [
    url(r'^$', list_cwd_file, name='pwd'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^images/', include('image_server.urls', namespace='images')),
]
