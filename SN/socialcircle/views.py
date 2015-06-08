from django.shortcuts import render,get_object_or_404,render_to_response,RequestContext
from django.http import HttpRequest,HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,hashers,decorators,logout
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
                    return HttpResponseRedirect('/socialcircle/dash/%s/' %user.id)
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

@decorators.login_required(login_url='/socialcircle/')
def dash(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)
    post = []
    for i in SCUser.objects.filter(user=scuser_id)[:]:
        for k in Post.objects.filter(post_user=i.pk)[:].order_by('-post_date')[:5]:
            tupla = (k,i)
            post.append(tupla)

  #  for i in user.post_set.order_by('-post_date')[:]:
   #     post.append(i)


    post_liked = []
    for i in xrange(len(user.like_set.values())):
        post_liked.append( user.like_set.values()[i].values()[3])


    #print post
    if request.method == 'POST':
        if "logout" in request.POST or "logout_menu" in request.POST:
            logout(request)
            return HttpResponseRedirect('/socialcircle/')
        elif "profile" in request.POST:
            return HttpResponseRedirect('/socialcircle/profile/%s/' %user.id)
        elif "like_post" in request.POST:
            #sel_post = user.post_set.get(pk=request.POST['like_post'])
            #new_like = Like(like_post=sel_post, like_user=user)
            #new_like.save()
            return render(request,'socialcircle/dashboard.html',{'scuser':user, 'post': post,'post_liked' : post_liked} ) #FIXME non me gusta molto che ricarica tutta la pag
        elif "unlike_post" in request.POST:
            #sel_like = user.like_set.get(like_post=request.POST['unlike_post'])
            #sel_like.delete()
            #sel_like.save()
            return render(request,'socialcircle/dashboard.html',{'scuser':user, 'post': post, 'post_liked' : post_liked} ) #FIXME non me gusta molto che ricarica tutta la pag
        elif "share" in request.POST:
            pass

    return render(request,'socialcircle/dashboard.html',{'scuser':user,'post':post,'post_liked' : post_liked})

def profile(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)

    post_liked = []
    for i in xrange(len(user.like_set.values())):
        post_liked.append( user.like_set.values()[i].values()[3])


    post_orderd = user.post_set.order_by('-post_date')[:]

    if request.method == 'POST':
        if "photos" in request.POST:
            return HttpResponseRedirect("photos/" )
        elif "videos" in request.POST:
            return HttpResponseRedirect("videos/" )
        elif "settings" in request.POST:
            return HttpResponseRedirect("settings/" )
        elif "likes" in request.POST:
            return HttpResponseRedirect("likes/" )
        elif "home" in request.POST:
            return HttpResponseRedirect("/socialcircle/dash/%s" %scuser_id ) #FIXME come recuperare id dell'utente loggato?
        elif "logout" in request.POST:
            logout(request)
            return HttpResponseRedirect('/socialcircle/')
        elif "like_post" in request.POST:
            #sel_post = user.post_set.get(pk=request.POST['like_post'])
            #new_like = Like(like_post=sel_post, like_user=user)
            #new_like.save()
            return render(request,'socialcircle/profile.html',{'scuser':user, 'post': post_orderd,'post_liked' : post_liked} ) #FIXME non me gusta molto che ricarica tutta la pag
        elif "unlike_post" in request.POST:
            #sel_like = user.like_set.get(like_post=request.POST['unlike_post'])
            #sel_like.delete()
            #sel_like.save()
            return render(request,'socialcircle/profile.html',{'scuser':user, 'post': post_orderd, 'post_liked' : post_liked} ) #FIXME non me gusta molto che ricarica tutta la pag
        elif "delete_post" in request.POST:
            sel_post = user.post_set.get(pk=request.POST['delete_post'])
            sel_post.delete()
            sel_post.save()
            return render(request,'socialcircle/profile.html',{'scuser':user, 'post': post_orderd, 'post_liked' : post_liked} ) #FIXME non me gusta molto che ricarica tutta la pag
    elif request.method == 'GET':
        return render(request,'socialcircle/profile.html',{'scuser':user, 'post': post_orderd, 'post_liked' : post_liked} )

def settings(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)
    if request.method == 'POST':
        form = modifyUser(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )
    else:
        form = modifyUser(instance=user)
    return render(request, 'socialcircle/settings.html', {'form': form,})

def photos(request,scuser_id):
    p = True
    user = get_object_or_404(SCUser,pk=scuser_id)

    if "back" in request.POST:
        return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )

    return render(request,'socialcircle/gallery.html', {'fl_p':p,'scuser':user})
def videos(request,scuser_id):
    p = False
    user = get_object_or_404(SCUser,pk=scuser_id)

    if "back" in request.POST:
        return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )

    return render(request,'socialcircle/gallery.html', {'fl_p':p,'scuser':user})
def likes(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)
    post_liked = user.like_set.order_by('-like_date')[:]
    if "back" in request.POST:
        return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )
    elif "unlike" in request.POST:
        pass
    return render(request,'socialcircle/likes.html', {'scuser':user, 'post_liked':post_liked})
