from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import ClassRoom
from .forms import ClassRoomForm
from django.contrib.auth.decorators import login_required

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
    
def class_create_step(request, classroom_id):
    classroom = ClassRoom.objects.get(pk=classroom_id)
    context = {'classroom':classroom}
    return render(request, 'classroom/steps.html', context)