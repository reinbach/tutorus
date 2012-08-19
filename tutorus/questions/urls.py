from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^(?P<classroom_id>\w+)/ask/$', views.ask_question, name='question_ask'),
    url(r'^(?P<question_id>\w+)/upvote/$', views.up_vote_question, name='question_up_vote'),
    url(r'^(?P<question_id>\w+)/answer/$', views.answer_question, name='question_answer'),
)