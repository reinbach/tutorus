from django.conf.urls import patterns, include, url
from .views import add, edit, delete

urlpatterns = patterns('',
    url(r'^add/(?P<classroom_id>\w+)/$', add, name='step_add'),
    url(r'^(?P<classroom_id>\w+)/delete/(?P<step_id>\w+)$', delete, name='step_delete'),
    url(r'^(?P<classroom_id>\w+)/edit/(?P<step_id>\w+)$', edit, name='step_edit'),
)