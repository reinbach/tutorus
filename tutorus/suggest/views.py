from .forms import SuggestForm
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def add(request):
    """
    add Suggestion
    """
    if request.method == 'POST':
        form = SuggestForm(request.POST)
        if form.is_valid():
            try:
                step = form.save()            
                return HttpResponseRedirect(reverse('home'))
            except Exception as e:
                #TODO: fix me.
                print("ERROR {0}".format(e))
        else:
            print form
    else:
        form = SuggestForm()

    context = {'form':form}
    return render(request, 'suggest/index.html', context)