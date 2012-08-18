from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from classroom.models import ClassRoom
from .models import Step
from .forms import StepForm
from django.contrib.auth.decorators import login_required


@login_required
def add(request, classroom_id):
    """
    add Step to classroom
    """
    #TODO do a 404 check here.
    classroom = ClassRoom.objects.get(pk=classroom_id)
    
    if request.method == 'POST':
        form = StepForm(request.POST)
        if form.is_valid():
            try:
                step = form.save(classroom)            
                return HttpResponseRedirect(reverse('class_create_step', args=[classroom.pk]))
            except Exception as e:
                #TODO: fix me.
                print("ERROR {0}".format(e))
        else:
            print form
    else:
        form = StepForm()

    context = {'form':form, 'classroom': classroom}
    return render(request, 'step/add.html', context)
    
@login_required
def edit(request, classroom_id, step_id):
    """
    add Step to classroom
    """
    #TODO do a 404 check here.
    classroom = ClassRoom.objects.get(pk=classroom_id)
    step = Step.objects.get(pk=step_id)

    if request.method == 'POST':
        form = StepForm(request.POST, instance=step)
        if form.is_valid():
            try:
                step = form.save(classroom)            
                return HttpResponseRedirect(reverse('class_create_step', args=[classroom.pk]))
            except Exception as e:
                #TODO: fix me.
                print("ERROR {0}".format(e))
        else:
            print form
    else:
        form = StepForm(instance=step)

    context = {'form':form, 'classroom': classroom}
    return render(request, 'step/add.html', context)