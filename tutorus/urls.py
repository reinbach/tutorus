from django.conf.urls import patterns, include, url

from user.forms import SignupFormExtra

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tutorus.views.home', name='home'),
    # url(r'^tutorus/', include('tutorus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    # Override the signup form with our own, which includes a first and last name.
    (r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    (r'^accounts/', include('userena.urls')),
    (r'^messages/', include('userena.contrib.umessages.urls')),
)
