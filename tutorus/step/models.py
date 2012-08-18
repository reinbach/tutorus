from django.db import models
from django.utils.translation import ugettext_lazy as _
from classroom.models import ClassRoom


class Step(models.Model):
    """ Steps for a ClassRoom
    """
    name = models.CharField(_('name'), max_length=50, blank=True)
    step_order = models.PositiveSmallIntegerField()
    content = models.TextField(blank=True, null=True, default="")
    classroom = models.ForeignKey(ClassRoom)
