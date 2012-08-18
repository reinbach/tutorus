# -*- coding: utf-8 -*-

"""

    classroom.tests.test_forms
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    'tests' for classroom forms

"""
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from dingus import Dingus
from classroom.forms import ClassRoomForm

from classroom.models import ClassRoom


__docformat__ = 'restructuredtext en'


class ClassRoomFixture(TestCase):

    @property
    def faux_user(self):
        return User.objects.get_or_create(username='faux_user')[0]

    data = {'name': 'ClassRoom Name',
            'tutor': Dingus(),
            'description': 'ClassRoom Description',
            'status': ClassRoom.STATUS.draft}

    def setUp(self):
        self.form = ClassRoomForm(self.data)

    def test_valid_form(self):
        self.assertTrue(self.form.is_valid())

    def test_save_form(self):
        classroom = self.form.save(self.faux_user)
        self.assertTrue(isinstance(classroom, ClassRoom))
        self.assertEquals(classroom.status, ClassRoom.STATUS.draft)
        self.assertEquals(classroom.tutor, self.faux_user)


class WhenClassRoomStatusNotPassed(ClassRoomFixture):

    data = {'name': 'ClassRoom Name',
            'tutor': Dingus(),
            'description': 'ClassRoom Description'}
