from django.test import TestCase

from questions.models import Question, ASKED


class QuestionsFixture(TestCase):

    subject = expected_subject = "What is the meaining of life?"
    def setUp(self):
        self.question = Question(
            subject=self.subject
        )

    def test_it_exists(self):
        self.assertEquals(self.question.subject, self.expected_subject)
        self.assertEquals(self.question.status, ASKED)
        self.assertEquals(self.question.content, "")