# -*- coding: utf-8 -*-

"""

    classroom.tests.test_views.test_class_activate
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    `class_activate` view unit tests

"""
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

__docformat__ = 'restructuredtext en'


class UnauthorizedRedirectedClassActivate(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('class_activate',
                                                args={'0', }))

    def test_response(self):
        self.assertEquals(self.response.status_code, 302)
        self.assertIn('/accounts/signin/?next=/class/0/activate',
                      self.response['location'])
