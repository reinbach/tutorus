from django.conf.urls import patterns, include, url
from .views import create_classroom, class_create_step

urlpatterns = patterns('',
    url(r'^create/$', create_classroom, name='create_classroom'),
    url(r'^(?P<classroom_id>\w+)/$', class_create_step, name='class_create_step'),
)