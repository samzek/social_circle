from django.shortcuts import render,get_object_or_404,render_to_response,RequestContext
from django.http import HttpRequest,HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,hashers,decorators,logout
from .models import SCUser,Post,Like

from django.core.urlresolvers import reverse
from forms import modifyUser, insertFile

# Create your views here.

def addLike(request):
    sel_post = Post.objects.get(pk=request.POST['like_post'])
    new_like = Like.objects.create(like_post=sel_post, like_user=request.user)
    new_like.save()
def deleteLike(request):
   # sel_post = Post.objects.get(pk=request.POST['unlike_post'])
    print "inside delete: ",request.POST['unlike_post']
    sel_post = get_object_or_404(Post,pk=request.POST['unlike_post'])
    sel_like = Like.objects.filter(like_post=sel_post,like_user=request.user)
    sel_like.delete()

def sharePost(request):
    sel_post = Post.objects.get(pk=request.POST['share'])
    p_t = sel_post.post_type
    cont = sel_post.content
    f = sel_post.file

    u = SCUser.objects.get(pk=request.user.id)
    new_post = Post.objects.create(content=cont, post_type=p_t,file=f)
    new_post.post_user.add(u)
    new_post.save()

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

            new_user.user.add(new_user)
            new_user.save()
            return HttpResponseRedirect('/socialcircle/')
    else:
        form = modifyUser()
    return render_to_response('socialcircle/reg.html', {'form': form}, context_instance=RequestContext(request))



unknow_user_list = []
@decorators.login_required(login_url='/socialcircle/')
def dash(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)
    if user.pk != request.user.id:
        return HttpResponseRedirect('/socialcircle/dash/%s/' %request.user.id)
    post = []
    global unknow_user_list
    for i in SCUser.objects.filter(user=scuser_id)[:]:
        for k in Post.objects.filter(post_user=i.pk)[:].order_by('-post_date')[:5]:
            tupla = (k,i)
            post.append(tupla)



    post_liked = []
    for i in xrange(len(request.user.like_set.values())):
        post_liked.append(request.user.like_set.values()[i].values()[3])

    #print post
    if request.method == 'POST':
        if "logout" in request.POST or "logout_menu" in request.POST:
            unknow_user_list = []
            logout(request)
            return HttpResponseRedirect('/socialcircle/')
        elif "profile" in request.POST:
            return HttpResponseRedirect('/socialcircle/profile/%s/' %user.id)
        elif "like_post" in request.POST:
            addLike(request)
            return HttpResponseRedirect('')
        elif "unlike_post" in request.POST:
            deleteLike(request)
            return HttpResponseRedirect('')
        elif "share" in request.POST:
            sharePost(request)
            return HttpResponseRedirect('')
        elif "submit_text" in request.POST:
            u = SCUser.objects.get(pk=request.user.id)
            new_post = Post.objects.create(content=request.POST['text_post'],post_type='is_text')
            new_post.post_user.add(u)
            new_post.save()
            return HttpResponseRedirect('')
        elif "res_user" in request.POST:
            unknow_user_list = []
            user_name = request.POST['res_user']
            first = user_name.split(' ')[0]
            second = user_name.split(' ')[1]
            for i in SCUser.objects.filter(first_name=first,last_name=second)[:]:
                unknow_user_list.append(i)
            return HttpResponseRedirect('')
        elif "submit_photo" in request.POST:
            u = SCUser.objects.get(pk=request.user.id)
            form = insertFile(request.POST, request.FILES)
            if form.is_valid():
                new_post= form.save(commit=False)
                new_post.post_type='is_photo'
                new_post.save()
                new_post.post_user.add(u)
                new_post.save()
                return HttpResponseRedirect('')
        elif "submit_video" in request.POST:
            u = SCUser.objects.get(pk=request.user.id)
            form = insertFile(request.POST, request.FILES)
            if form.is_valid():
                new_post= form.save(commit=False)
                new_post.post_type='is_video'
                new_post.save()
                new_post.post_user.add(u)
                new_post.save()
                return HttpResponseRedirect('')

    form = insertFile()
    return render(request,'socialcircle/dashboard.html',{'scuser':user,'post':post,'post_liked' : post_liked,'unknow':unknow_user_list, 'form':form})





def profile(request,scuser_id):
    global unknow_user_list
    user = get_object_or_404(SCUser,pk=scuser_id)

    friend_list = []
    for i in SCUser.objects.filter(user=request.user.id)[:]:
        friend_list.append(i.pk)

    #TODO creare una lista con i tre amici da visualizzare nella pagina del profilo

    post_liked = []
    for i in xrange(len(request.user.like_set.values())):
        post_liked.append( request.user.like_set.values()[i].values()[3])

    post_orderd = user.post_set.order_by('-post_date')[:]

    data = {'scuser':user, 'post': post_orderd, 'post_liked' : post_liked, 'curr_user':request.user, 'friends':friend_list}

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
            return HttpResponseRedirect("/socialcircle/dash/%s" %request.user.id )
        elif "logout" in request.POST:
            unknow_user_list = []
            logout(request)
            return HttpResponseRedirect('/socialcircle/')
        elif "like_post" in request.POST:
            addLike(request)
            return HttpResponseRedirect('')
        elif "unlike_post" in request.POST:
            deleteLike(request)
            return HttpResponseRedirect('')
        elif "delete_post" in request.POST:
            sel_post = user.post_set.get(pk=request.POST['delete_post'])
            sel_post.delete()
            sel_post.save()
            return HttpResponseRedirect('')
        elif "share" in request.POST:
            sharePost(request)
            return HttpResponseRedirect('')
        elif "add_friend" in request.POST:
            friend = SCUser.objects.get(pk = request.POST['add_friend'])
            request.user.user.add(friend)
            return HttpResponseRedirect('')
        elif "del_friend" in request.POST:
            friend = SCUser.objects.get(pk = request.POST['del_friend'])
            request.user.user.remove(friend)
            return HttpResponseRedirect('')
        elif "all_friends" in request.POST:
            return HttpResponseRedirect("/socialcircle/profile/%s/friends" %scuser_id )

    elif request.method == 'GET':
        return render(request,'socialcircle/profile.html',data )



def settings(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)
    if user.pk != request.user.id:
        return HttpResponseRedirect('/socialcircle/profile/%s/settings' %request.user.id)

    if request.method == 'POST':
        form = modifyUser(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )
    else:
        form = modifyUser(instance=user)
    return render(request, 'socialcircle/settings.html', {'form': form,})




def photos(request,scuser_id):
    p = True
    user = get_object_or_404(SCUser,pk=scuser_id)

    post_orderd = user.post_set.order_by('-post_date')[:]

    if "back" in request.POST:
        return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )

    return render(request,'socialcircle/gallery.html', {'fl_p':p,'scuser':user,'post':post_orderd})




def videos(request,scuser_id):
    p = False
    user = get_object_or_404(SCUser,pk=scuser_id)

    post_orderd = user.post_set.order_by('-post_date')[:]

    if "back" in request.POST:
        return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )

    return render(request,'socialcircle/gallery.html', {'fl_p':p,'scuser':user,'post':post_orderd})


def likes(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)
    if user.pk != request.user.id:
        return HttpResponseRedirect('/socialcircle/profile/%s/likes' %request.user.id)

    post_liked = request.user.like_set.order_by('-like_date')
    if "back" in request.POST:
        return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )
    elif "unlike_post" in request.POST:
        deleteLike(request)
        return HttpResponseRedirect('')

    return render(request,'socialcircle/likes.html', {'scuser':user, 'post_liked':post_liked})

def friends(request,scuser_id):
    user = get_object_or_404(SCUser,pk=scuser_id)
    curr_user = request.user
    if "back" in request.POST:
        return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )
    return render(request,'socialcircle/friends.html', {'scuser':user, 'curr_user':curr_user})