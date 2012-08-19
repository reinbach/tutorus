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
    def student_user(self):
        return User.objects.get_or_create(username='student_user')[0]

    @property
    def tutor_user(self):
        return User.objects.get_or_create(username='tutor_user')[0]

    @property
    def classroom_steps(self):
        return None

    @property
    def classroom(self):
        classroom = ClassRoom(name='My classroom',
                              tutor=self.tutor_user,
                              description='My classroom description')
        classroom.save()
        return classroom

    def setUp(self):
        self.classroom


class WhenInitialClassroomIsCreated(ClassRoomFixture):

    def test_it(self):
        self.assertEquals(self.classroom.name, 'My classroom')
        self.assertEquals(self.classroom.tutor, self.tutor_user)
        self.assertEquals(self.classroom.description,
                          'My classroom description')


class InitialClassRoomsDoNotHaveSteps(ClassRoomFixture):

    def setUp(self):
        self.steps = self.classroom.steps

    def test_it(self):
        self.assertEquals(len(self.steps), 0)


class InitialClassRoomsAreNotActive(ClassRoomFixture):

    def setUp(self):
        self.is_active = self.classroom.is_active()

    def test_it(self):
        self.assertFalse(self.is_active)


class TutorUserIsTheTutor(ClassRoomFixture):

    def setUp(self):
        self.is_tutor = self.classroom.is_tutor(self.tutor_user)

    def test_it(self):
        self.assertTrue(self.is_tutor)


class StudentUserIsNotTheTutor(ClassRoomFixture):

    def setUp(self):
        self.is_tutor = self.classroom.is_tutor(self.student_user)

    def test_it(self):
        self.assertFalse(self.is_tutor)
