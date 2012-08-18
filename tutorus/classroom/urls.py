from django.conf.urls import patterns, url

urlpatterns = patterns(
    'classroom.views',
    url(r'^create/$', 'create', name='classroom_create'),
    url(r'^$', 'home', name='classroom_home'),
)