# -*- coding: utf-8 -*-

"""

    scratchpad.forms
    ~~~~~~~~~~~~~~~~

    `forms` used for the scratchpads

"""
from django import forms
from django.forms.widgets import HiddenInput

from scratchpad.models import Scratchpad

__docformat__ = 'restructuredtext en'


class ScratchpadForm(forms.ModelForm):

    # todo not ideal, but quick?
    classroom = forms.IntegerField(widget=HiddenInput)

    class Meta:
        model = Scratchpad

    def clean_classroom(self):
        """ We handle unique classrooms in save """
        return self.cleaned_data['classroom']

    def clean(self):
        return self.cleaned_data

    def save(self, classroom, *args, **kwargs):
        scratchpad, r = Scratchpad.objects.get_or_create(classroom=classroom)
        if 'content' in self.cleaned_data:
            scratchpad.content = self.cleaned_data['content']
        scratchpad.save()
