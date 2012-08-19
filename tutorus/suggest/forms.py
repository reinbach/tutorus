from django import forms
from .models import Suggestion

class SuggestForm(forms.ModelForm):
    
    class Meta:
        model = Suggestion