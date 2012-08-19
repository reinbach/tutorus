from django import forms

from models import Question

class AskQuestionForm(forms.ModelForm):
    subject = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea())
    
    class Meta:
        model = Question
        exclude=('classroom', 'status', 'student',)

    def save(self, user, classroom, commit=True):
        question = super(AskQuestionForm, self).save(commit=False)
        question.student = user
        question.classroom = classroom
        question.save()
        return question