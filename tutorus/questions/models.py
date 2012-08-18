from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from classroom.models import ClassRoom
from questions import constants


class Question(models.Model):

    class Meta:
        ordering = ("-created",)

    subject = models.CharField(_('Subject'), max_length=50, blank=False,
                               null=False, default="")
    content = models.TextField(_('Content'), blank=True, null=True, default="")
    status = models.CharField(max_length=10,
                              choices=constants.QUESTION_CHOICES,
                              default=constants.ASKED)
    classroom = models.ForeignKey(ClassRoom, blank=None, null=True)
    student = models.ForeignKey(User, verbose_name=_('student'))
    created = models.DateTimeField(auto_now_add=True)


class QuestionVotes(models.Model):
    question = models.ForeignKey(Question)
    voter = models.ForeignKey(User, verbose_name=_('voter'))