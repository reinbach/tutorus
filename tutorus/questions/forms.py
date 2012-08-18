from django import forms

from models import Question

class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude=('classroom', 'status', 'student',)

    def save(self, user, commit=True):
        question = super(AskQuestionForm, self).save(commit=False)
        question.student = user
        question.save()
        return question