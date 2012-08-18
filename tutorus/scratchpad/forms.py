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
        exclude = ('classroom',)
