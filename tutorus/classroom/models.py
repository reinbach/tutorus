import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from model_utils.fields import StatusField
from model_utils import Choices
from model_utils.models import TimeStampedModel

from questions import constants as question_constants
from utils import slugify_uniquely

log = logging.getLogger(__name__)


class ClassRoom(TimeStampedModel):
    """ ClassRoom
    """
    STATUS = Choices('draft', 'active', 'closed')

    name = models.CharField(_('name'), max_length=255, blank=True)
    slug = models.SlugField(null=True, blank=True, default="", unique=True)
    tutor = models.ForeignKey(User, verbose_name=_('tutor'))
    description = models.TextField(blank=True, null=True, default="")
    status = StatusField(default=STATUS.draft)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super(ClassRoom, self).save(*args, **kwargs)

    @property
    def steps(self):
        return self.step_set.all()

    def is_active(self):
        return True if self.status == "active" else False

    def is_tutor(self, user):
        if user == self.tutor:
            return True
        return False

    def latest_unanswered_questions(self, user=None):
        """Get list of new questions that have not been answered

        Also if we know the user, then exclude those questions
        that have been voted by the user already
        """
        latest_list = self.question_set.filter(
            status=question_constants.ASKED
        )

        # if we have the user we need to exclude those questions
        # user has already voted for
        if user is not None:
            from questions.models import QuestionVotes
            questions_voted_for_list = QuestionVotes.objects.values_list(
                "question__pk"
            ).filter(voter=user)
            latest_list = latest_list.exclude(
                pk__in=[x[0] for x in questions_voted_for_list]
            )

        return latest_list[:settings.LATEST_QUESTIONS_COUNT]

    def top_questions(self):
        """Get list of top questions for the classroom

        Top is determined by the vote count for the question
        """
        from questions.models import QuestionVotes
        top_list = QuestionVotes.objects.filter(
            question__classroom=self,
            question__status=question_constants.ASKED
        ).annotate(num_votes=Count("question")).order_by("num_votes")
        top_list = [x.question for x in top_list]
        return top_list[:settings.TOP_QUESTIONS_COUNT]

    def answered_questions(self):
        """Get a list of the answered questions"""
        return self.question_set.filter(
            status=question_constants.ANSWERED
        )

    def interest(self):
        """Get level of interest in class"""
        return ClassRoomStudentInterest.objects.filter(
            classroom=self
        ).count()


class ClassRoomStudentInterest(models.Model):
    """Track students that are interested in the classroom"""
    classroom = models.ForeignKey(ClassRoom)
    student = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
