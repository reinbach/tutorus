from django.db import models

from classroom.models import ClassRoom


class Scratchpad(models.Model):
    """ Scratch pad
    """
    content = models.TextField(blank=True, null=True, default="")
    classroom = models.OneToOneField(ClassRoom, blank=None, null=True)
