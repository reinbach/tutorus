from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from model_utils.fields import StatusField
from model_utils import Choices
from model_utils.models import TimeStampedModel

from questions import constants as question_constants

LATEST_QUESTIONS_COUNT = 10

class ClassRoom(TimeStampedModel):
    """ ClassRoom
    """
    STATUS = Choices('draft', 'active', 'closed')

    name =  models.CharField(_('name'), max_length=255, blank=True)
    tutor = models.ForeignKey(User, verbose_name=_('tutor'))
    description = models.TextField(blank=True, null=True, default="")
    status = StatusField(default=STATUS.draft)

    @property
    def steps(self):
        return self.step_set.all()

    def is_active(self):
        return True if self.status == "active" else False

    def is_tutor(self, user):
        if user == self.tutor:
            return True
        return False

    def latest_unanswered_questions(self):
        return self.question_set.filter(
            status=question_constants.ASKED
        )[:LATEST_QUESTIONS_COUNT]