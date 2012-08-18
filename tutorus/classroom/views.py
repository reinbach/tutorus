import logging

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import ClassRoom
from .forms import ClassRoomForm

log = logging.getLogger(__name__)

@login_required
def create_classroom(request):
    """
    Create ClassRoom
    """
    if request.method == 'POST':
        form = ClassRoomForm(request.POST)
        if form.is_valid():
            try:
                classroom = form.save(request.user)
                return HttpResponseRedirect(reverse('class_create_step', args=[classroom.pk]))
            except Exception as e:
                #TODO: fix me.
                print("ERROR {0}".format(e))
        else:
            print form
    else:
        form = ClassRoomForm()

    context = {'form':form}
    return render(request, 'classroom/create.html', context)

#TODO limit access to classroom to only tutor
def class_create_step(request, classroom_id):
    classroom = ClassRoom.objects.get(pk=classroom_id)
    context = {'classroom': classroom}
    return render(request, 'classroom/steps.html', context)

def class_activate(request, classroom_id):
    classroom = ClassRoom.objects.get(pk=classroom_id)
    #test
    log.info(classroom.status)
    classroom.status = 'active'
    classroom.save()
    context = {'classroom': classroom}
    return render(request, 'classroom/steps.html', context)

def home(request):
    context = dict(
        classrooms=ClassRoom.objects.all() # so we get something change later filter(status='active')
    )
    return render(request, "classroom/index.html", context)