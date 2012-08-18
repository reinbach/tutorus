from django.forms import ModelForm
from .models import ClassRoom

class ClassRoomForm(ModelForm):
    class Meta:
        model = ClassRoom
        exclude=('status', 'tutor',)

    def save(self, user, commit=True):

        classroom= super(ClassRoomForm, self).save(commit=False)
        classroom.tutor = user
        classroom.status = ClassRoom.STATUS.draft
        classroom.save()

        return classroom

