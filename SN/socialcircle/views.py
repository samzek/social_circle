from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest,HttpResponseRedirect, HttpResponse
from .models import SCUser,Post,Like,Cat
from django.core.urlresolvers import reverse
from socialcircle.forms import modifyUser

# Create your views here.

def index(request):
    return render(request,'socialcircle/index.html')
def dash(request,scuser_id):
    return render(request,'socialcircle/dashboard.html')
def profile(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)

    if request.method == 'POST':
        if "photos" in request.POST:
            return HttpResponseRedirect("photos/" )
        elif "videos" in request.POST:
            return HttpResponseRedirect("videos/" )
        elif "settings" in request.POST:
            return HttpResponseRedirect("settings/" )
        elif "likes" in request.POST:
            return HttpResponseRedirect("likes/" )
    elif request.method == 'GET':
        return render(request,'socialcircle/profile.html',{'scuser':user})

def settings(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)
    if request.method == 'POST':
        form = modifyUser(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )
    else:  # GET request: just visualize the form
        form = modifyUser(instance=user)
    return render(request, 'socialcircle/settings.html', {'form': form,})

def photos(request,scuser_id):
    p = True
    user = get_object_or_404(SCUser,pk=scuser_id)

    return render(request,'socialcircle/gallery.html', {'fl_p':p,'scuser':user})
def videos(request,scuser_id):
    p = False
    user = get_object_or_404(SCUser,pk=scuser_id)

    return render(request,'socialcircle/gallery.html', {'fl_p':p,'scuser':user})
def likes(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)
    if request.method == 'POST':
        return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )
    return render(request,'socialcircle/likes.html', {'scuser':user})
