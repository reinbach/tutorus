from django.db import models

class Scratchpad(models.Model):
    """ Scratch pad
    """
    content = models.TextField(blank=True, null=True, default="")
    # class = models.ForeignKey(Class)
