import json
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from core.utils import publish
from questions.forms import AskQuestionForm
from scratchpad.forms import ScratchpadForm
from scratchpad.models import Scratchpad
from step.models import Step

from .models import ClassRoom, ClassRoomStudentInterest
from .forms import ClassRoomForm

log = logging.getLogger(__name__)


def tutor_only(func):
    def decorator(request, classroom_id, *args, **kwargs):
        classroom = ClassRoom.objects.get(pk=classroom_id)
        if classroom.is_tutor(request.user):
            return func(request, classroom, *args, **kwargs)
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
    interest, created = ClassRoomStudentInterest.objects.get_or_create(
        student=request.user,
        classroom=classroom
    )
    # publish interest to class channel, only if interest added
    if created:
        channel = "classes"
        message = {
            "type": "interest",
            "classroom": classroom.pk,
            "interest": classroom.interest(),
        }
        publish(channel, message)
    return HttpResponse(json.dumps({"success": True}))


@login_required
def class_list(request):
    """List of classes for tutor

    If there are no classes, redirect to user appropriately
     - if coming from create page, then go home
     - other to decision page (find / create)
    """
    tutoring_list = list(ClassRoom.objects.filter(
        tutor=request.user).values_list('pk', flat=True))
    interested_list = list(ClassRoomStudentInterest.objects.filter(
        student=request.user).values_list('classroom', flat=True))
    classrooms = ClassRoom.objects.filter(pk__in=tutoring_list+interested_list)

    if not classrooms.exists():
        # if being redirected from create class
        # head to home page instead, no need to send
        # user back to where they came from
        if "from" in request.GET and request.GET['from'] == "create":
            return HttpResponseRedirect(reverse("home"))
        return render(request, "classroom/decision.html", {})
    context = dict(
        classrooms=classrooms,
        page="class",
        user=request.user,
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
        context.update(is_tutor=True)
        return render(request, "classroom/take.html", context)
    context.update(
        question_form=AskQuestionForm()
    )
    return render(request, "classroom/take_student.html", context)

@login_required
@tutor_only
def class_scratchpad(request, classroom):
    """Publish scratchpad to students"""
    if request.method == 'POST':
        form = ScratchpadForm(data=request.POST)
        if form.is_valid():
            message = {"success": True}
            channel = "classroom_{0}".format(classroom.pk)
            pub_message = {
                "type": "scratchpad",
                "data": form.cleaned_data['content']
            }
            publish(channel, pub_message)
        else:
            message = {"error": form.errors}
            return HttpResponseBadRequest(message)
        return HttpResponse(json.dumps(message))
    return HttpResponseNotFound("Need to post")

@login_required
@tutor_only
def class_step(request, classroom, step_id):
    step = get_object_or_404(Step, pk=step_id)
    channel = "classroom_{0}".format(classroom.pk)
    pub_message = {
        "type": "step",
        "data": {
            "step": step.pk,
            "content": step.content
        }
    }
    publish(channel, pub_message)
    return HttpResponse(json.dumps({"success": True}))

def home(request):
    context = dict(
        classrooms=ClassRoom.objects.filter(status='active')
    )
    if request.user.is_authenticated():
        interest_list = ClassRoomStudentInterest.objects.values_list(
            "classroom__pk"
        ).filter(student=request.user)
        context.update(interest_list=[x[0] for x in interest_list])
    return render(request, "classroom/index.html", context)
