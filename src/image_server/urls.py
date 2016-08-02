from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.list_cwd_file, name='list'),
    url('^remove$', views.remove_specify_file, name='remove'),
    url('^removed/(?P<filename>.+)/$', views.removed, name='removed')
]
