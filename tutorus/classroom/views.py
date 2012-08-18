import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import ClassRoom
from .forms import ClassRoomForm

log = logging.getLogger(__name__)

def tutor_only(func):
    def decorator(request, classroom_id):
        classroom = ClassRoom.objects.get(pk=classroom_id)
        if classroom.is_tutor(request.user):
            return func(request, classroom)
        messages.info(request, "You are not the Tutor")
        return HttpResponseRedirect(reverse('class_home'))
    return decorator

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
    
@login_required
@tutor_only
def edit_classroom(request, classroom):
    """
    Edit ClassRoom
    """
    if request.method == 'POST':
        form = ClassRoomForm(request.POST, instance=classroom)
        if form.is_valid():
            try:
                classroom = form.save(request.user)
                return HttpResponseRedirect(reverse('class_create_step', args=[classroom.pk]))
            except Exception as e:
                #TODO: fix me.
                print("ERROR {0}".format(e))
        else:
            #TODO do something better with errors
            print form
    else:
        form = ClassRoomForm(instance=classroom)

    context = {'form':form}
    return render(request, 'classroom/create.html', context)

@login_required
@tutor_only
def class_create_step(request, classroom):
    context = {'classroom': classroom}
    return render(request, 'classroom/steps.html', context)

@login_required
@tutor_only
def class_activate(request, classroom):
    classroom.status = 'active'
    classroom.save()
    context = {'classroom': classroom}
    return render(request, 'classroom/steps.html', context)

@login_required
@tutor_only
def class_take(request, classroom):
    """Take the class

    Different experience based on whether tutor or student
    """
    context = dict(
        classroom=classroom
    )
    #test
    log.info(request.user)
    if classroom.is_tutor(request.user):
        context.update(tutor=True)
        return render(request, "classroom/take.html", context)
    return render(request, "classroom/take_student.html", context)

def home(request):
    context = dict(
        classrooms=ClassRoom.objects.all() # so we get something change later filter(status='active')
    )
    return render(request, "classroom/index.html", context)