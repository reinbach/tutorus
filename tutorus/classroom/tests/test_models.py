# -*- coding: utf-8 -*-

"""

    classroom.tests.test_models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    `model` tests

"""
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from classroom.models import ClassRoom

__docformat__ = 'restructuredtext en'


class ClassRoomFixture(TestCase):

    @property
    def faux_user(self):
        return User.objects.get_or_create(username='faux_user')[0]

    @property
    def classroom(self):
        classroom = ClassRoom(name='My classroom',
                              tutor=self.faux_user,
                              description='My classroom description')
        classroom.save()
        return classroom

    def setUp(self):
        self.classroom

    def test_it(self):
        self.assertEquals(self.classroom.name, 'My classroom')
        self.assertEquals(self.classroom.tutor, self.faux_user)
        self.assertEquals(self.classroom.description,
                          'My classroom description')