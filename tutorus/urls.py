from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from user.forms import SignupFormExtra

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    (r'^classroom/', include('classroom.urls')),
    # Override the signup form with our own, which includes a first and last name.
    (r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    (r'^accounts/', include('userena.urls')),
    (r'^messages/', include('userena.contrib.umessages.urls')),
    (r'^class/', include('classroom.urls')),
    (r'^step/', include('step.urls')),
)

urlpatterns += staticfiles_urlpatterns()