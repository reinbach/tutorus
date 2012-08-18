from django import forms

from models import ClassRoom

class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom