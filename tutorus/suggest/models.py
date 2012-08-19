from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

class Suggestion(TimeStampedModel):
    """ suggest class
    """
    name = models.CharField(_('name'), max_length=255, blank=True)
    email = models.EmailField(_('email'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True, null=True, default="")

