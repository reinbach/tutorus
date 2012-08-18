from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^(?P<classroom_id>\w+)/ask/$', views.ask_question, name='question_ask'),
)