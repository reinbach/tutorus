from django import http
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render

from forms import ClassRoomForm
from models import ClassRoom

def home(request):
    context = dict(
        classrooms=ClassRoom.objects.filter(status='active')
    )
    return render(request, "classroom/index.html", context)

@login_required
def create(request):
    form = ClassRoomForm()
    if request.method == 'POST':
        form = ClassRoomForm(data=request.POST)
        if form.is_valid():
            return http.ResponseRedirect(reverse('classroom_home'))
    context = dict(
        form=form
    )
    return render(request, "classroom/create.html", context)
