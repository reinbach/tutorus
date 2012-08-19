# -*- coding: utf-8 -*-

"""

    scratchpad.forms
    ~~~~~~~~~~~~~~~~

    `forms` used for the scratchpads

"""
from django import forms

from scratchpad.models import Scratchpad

__docformat__ = 'restructuredtext en'


class ScratchpadForm(forms.ModelForm):

    class Meta:
        model = Scratchpad
        exclude = ("classroom",)

    def save(self, classroom, *args, **kwargs):
        scratchpad, r = Scratchpad.objects.get_or_create(classroom=classroom)
        if 'content' in self.cleaned_data:
            scratchpad.content = self.cleaned_data['content']
        scratchpad.save()
