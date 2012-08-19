# -*- coding: utf-8 -*-

"""

    classroom.tests.test_views.test_home
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    `home` view tests for classroom

"""
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

__docformat__ = 'restructuredtext en'


class SimpleNavigateToHome(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('class_home'))

    def test_response(self):
        self.assertEquals(self.response.status_code, 200)
        self.assertTrue('classrooms' in self.response.context)
        self.assertEquals(len(self.response.context['classrooms']), 0)
