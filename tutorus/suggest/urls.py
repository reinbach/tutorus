from django.conf.urls import patterns, include, url
from .views import add

urlpatterns = patterns('',
    url(r'^$', add, name='add_suggestion'),
)