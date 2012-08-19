# -*- coding: utf-8 -*-

"""

    classroom.tests.test_views.test_class_edit
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    `class_edit` view unit tests

"""
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

__docformat__ = 'restructuredtext en'


class UnauthorizedRedirectedClassEdit(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('class_edit',
                                                args={'0', }))

    def test_response(self):
        self.assertEquals(self.response.status_code, 302)
        self.assertIn('/accounts/signin/?next=/class/0/edit',
                      self.response['location'])
