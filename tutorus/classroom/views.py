import json
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

from core.utils import get_pubnub_connection
from questions.forms import AskQuestionForm
from scratchpad.forms import ScratchpadForm
from scratchpad.models import Scratchpad

from .models import ClassRoom, ClassRoomStudentInterest
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
                return HttpResponseRedirect(reverse('class_create_step',
                                                    args=[classroom.pk]))
            except Exception as e:
                #TODO: fix me.
                print("ERROR {0}".format(e))
        else:
            print form
    else:
        form = ClassRoomForm()

    context = {'form': form}
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
                return HttpResponseRedirect(reverse('class_create_step',
                                                    args=[classroom.pk]))
            except Exception as e:
                #TODO: fix me.
                print("ERROR {0}".format(e))
        else:
            #TODO do something better with errors
            print form
    else:
        form = ClassRoomForm(instance=classroom)

    context = {'form': form}
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
def class_interest(request, classroom_id):
    """Mark students interest in the class"""
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    interest, r = ClassRoomStudentInterest.objects.get_or_create(
        student=request.user,
        classroom=classroom
    )
    # publish interest to class channel
    pubnub = get_pubnub_connection()
    pubnub.publish({
        "channel": "tutor_{0}".format(classroom.tutor.pk),
        "message": {
            "type": "interest",
            "interest": classroom.interest(),
        }
    })
    return HttpResponse(json.dumps({"success": True}))

@login_required
def class_list(request):
    """List of classes for tutor

    If there are no classes, redirect to user appropriately
     - if coming from create page, then go home
     - other to decision page (find / create)
    """
    classrooms = ClassRoom.objects.filter(tutor=request.user)
    if not classrooms.exists():
        # if being redirected from create class
        # head to home page instead, no need to send
        # user back to where they came from
        if "from" in request.GET and request.GET['from'] == "create":
            return HttpResponseRedirect(reverse("home"))
        return render(request, "classroom/decision.html", {})
    context = dict(
        classrooms=classrooms,
        page="class"
    )
    return render(request, 'classroom/list.html', context)


@login_required
def class_take(request, classroom_id):
    """Take the class

    Different experience based on whether tutor or student
    """
    classroom = ClassRoom.objects.get(pk=classroom_id)
    if request.method == 'POST':
        scratchpad_form = ScratchpadForm(request.POST)
        if scratchpad_form.is_valid():
            scratchpad_form.save(classroom)
    else:
        scratchpad, r = Scratchpad.objects.get_or_create(classroom=classroom)
        scratchpad_form = ScratchpadForm(instance=scratchpad)

    context = dict(
        classroom=classroom,
        user=request.user,
        scratchpad_form=scratchpad_form,
        latest_questions_count=settings.LATEST_QUESTIONS_COUNT,
    )
    if classroom.is_tutor(request.user):
        context.update(tutor=True)
        return render(request, "classroom/take.html", context)
    context.update(
        question_form=AskQuestionForm()
    )
    return render(request, "classroom/take_student.html", context)


def home(request):
    context = dict(
        classrooms=ClassRoom.objects.filter(status='active')
    )
    return render(request, "classroom/index.html", context)
