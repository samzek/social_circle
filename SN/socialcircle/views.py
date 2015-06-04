from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest,HttpResponseRedirect, HttpResponse
from .models import SCUser,Post,Like,Cat

# Create your views here.

def index(request):
    return render(request,'socialcircle/index.html')
def dash(request,scuser_id):
    return render(request,'socialcircle/dashboard.html')
def profile(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)
    return render(request,'socialcircle/profile.html',{'scuser':user})
def settings(request,scuser_id):
    return render(request,'socialcircle/settings.html')
def photos(request,scuser_id):
    return render(request,'socialcircle/gallery.html')
def videos(request,scuser_id):
    return render(request,'socialcircle/gallery.html')
