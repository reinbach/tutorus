from django.conf.urls import patterns, include, url
from django.conf import settings

from user.forms import SignupFormExtra

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    # Override the signup form with our own, which includes a first and last name.
    (r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    (r'^accounts/', include('userena.urls')),
    (r'^messages/', include('userena.contrib.umessages.urls')),
)

if settings.DEBUG:
    # conditionally serve static files
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()