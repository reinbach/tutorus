from django.test import TestCase

from scratchpad.models import Scratchpad


class ScratchPadFixture(TestCase):

    expected = ""

    def setUp(self):
        self.scratchpad = Scratchpad()

    def test_scratchpad_created(self):
        self.assertEqual(self.scratchpad.content, self.expected)