from django.conf.urls import patterns, include, url
from .views import add, edit

urlpatterns = patterns('',
    url(r'^add/(?P<classroom_id>\w+)/$', add, name='step_add'),
    url(r'^(?P<classroom_id>\w+)/edit/(?P<step_id>\w+)$', edit, name='step_edit'),
)