from django.shortcuts import render,get_object_or_404,render_to_response,RequestContext
from django.http import HttpRequest,HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,hashers
from .models import SCUser,Post,Like,Cat

from django.core.urlresolvers import reverse
from forms import modifyUser

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
                    return render(request,'socialcircle/profile.html/',{'scuser':user})
                else:
                    return render(request,'socialcircle/index.html')
            else:
                print "USER NOT FOUND"
                return render(request,'socialcircle/index.html')
        else:
            return HttpResponseRedirect("reg/")
    return render(request,'socialcircle/index.html')

def reg(request):
    if request.method == 'POST':
        form = modifyUser(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.password = hashers.make_password(new_user.password,salt=None,hasher='default')
            new_user.save()
            return HttpResponseRedirect('/socialcircle/')
    else:
        form = modifyUser()
    return render_to_response('socialcircle/reg.html', {'form': form}, context_instance=RequestContext(request))

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
