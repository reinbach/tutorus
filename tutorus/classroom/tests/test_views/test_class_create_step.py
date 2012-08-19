# -*- coding: utf-8 -*-

"""

    classroom.tests.test_views.test_class_create_step
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    `create step` view tests

"""
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

__docformat__ = 'restructuredtext en'


class UnauthorizedRedirectedClassCreateStep(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('class_create_step',
                                                args={'0',}))

    def test_response(self):
        self.assertEquals(self.response.status_code, 302)
        self.assertIn('/accounts/signin/?next=/class/0/',
                      self.response['location'])
