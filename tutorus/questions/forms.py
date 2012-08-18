from django import forms

from models import Question

class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude=('classroom', 'status', 'student',)

    def save(self, user, classroom, commit=True):
        question = super(AskQuestionForm, self).save(commit=False)
        question.student = user
        question.classroom = classroom
        question.save()
        return question