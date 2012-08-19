# -*- coding: utf-8 -*-

"""

    classroom.tests.tests_views.test_create_classroom
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    `create_classroom` view unit tests

"""
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

__docformat__ = 'restructuredtext en'

class UnauthorizedUsersRedirectedToLogin(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('class_create'))

    def test_response(self):
        self.assertEquals(self.response.status_code, 302)
        self.assertIn('/accounts/signin/?next=/class/create/',
                      self.response['location'])

