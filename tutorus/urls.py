from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from user.forms import SignupFormExtra

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^classroom/', include('classroom.urls')),
    url(r'^question/', include('questions.urls')),
    # Override the signup form with our own, which includes a first and last name.
    (r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    (r'^accounts/', include('userena.urls')),
    (r'^messages/', include('userena.contrib.umessages.urls')),
    (r'^class/', include('classroom.urls')),
    (r'^step/', include('step.urls')),
    (r'^suggest/', include('suggest.urls')),
)

urlpatterns += staticfiles_urlpatterns()