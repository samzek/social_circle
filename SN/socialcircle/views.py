from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest,HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login
from .models import SCUser,Post,Like,Cat

from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
    if request.method == 'POST':
        if "log_in" in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return render(request,'socialcircle/dashboard.html')
                else:
                    return render(request,'socialcircle/index.html')
            else:
                print "USER NOT FOUND"
                return render(request,'socialcircle/index.html')
        elif "sign" in request.POST:
            return render(request,'socialcircle/registration.html')

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
    return render(request,'socialcircle/settings.html')
def photos(request,scuser_id):
    return render(request,'socialcircle/gallery.html')
def videos(request,scuser_id):
    return render(request,'socialcircle/gallery.html')
def likes(request,scuser_id):
    return render(request,'socialcircle/likes.html')
