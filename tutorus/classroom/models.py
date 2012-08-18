from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import StatusField
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User

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