# -*- coding: utf-8 -*-

"""

    classroom.tests.test_templatetags
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    `templatetag` tests

"""
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from classroom.models import ClassRoom
from classroom.templatetags.classroom_tags import latest_questions

__docformat__ = 'restructuredtext en'


class WhenNoQuestionsForUser(TestCase):

    @property
    def tutor_user(self):
        return User.objects.get_or_create(username='tutor_user')[0]

    @property
    def classroom(self):
        classroom = ClassRoom(name='My classroom',
                              tutor=self.tutor_user,
                              description='My classroom description')
        classroom.save()
        return classroom

    def setUp(self):
        self.latest_questions = latest_questions(self.classroom,
                                                 self.tutor_user)

    def test_it(self):
        self.assertEqual(len(self.latest_questions['questions']), 0)
