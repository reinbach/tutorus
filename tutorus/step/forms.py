from django.forms import ModelForm, CharField
from .models import Step

class StepForm(ModelForm):
    name = CharField(required=True)

    class Meta:
        model = Step
        exclude = ('classroom','step_order')

    def save(self, classroom, commit=True):
        step= super(StepForm, self).save(commit=False)
        step.classroom = classroom
        step.step_order = 1 #todo, fix this.
        step.save()

        return step
        