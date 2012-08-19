from django import forms

from models import Question

class AskQuestionForm(forms.ModelForm):
    subject = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea())

    class Meta:
        model = Question
        exclude=('classroom', 'status', 'student', 'answer',)

    def save(self, user, classroom, commit=True):
        question = super(AskQuestionForm, self).save(commit=False)
        question.student = user
        question.classroom = classroom
        question.save()
        return question

class AnswerQuestionForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea)

    def save(self, question):
        question.answer = self.cleaned_data['answer']
        question.save()
        return question