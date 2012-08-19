from django.forms import ModelForm, CharField

from .models import ClassRoom

class ClassRoomForm(ModelForm):
    name = CharField(required=True)

    class Meta:
        model = ClassRoom
        exclude = ('status', 'tutor',)

    def save(self, user, commit=True):

        classroom = super(ClassRoomForm, self).save(commit=False)
        classroom.tutor = user
        classroom.save()

        return classroom
