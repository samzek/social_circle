from django.shortcuts import render,get_object_or_404,render_to_response,RequestContext
from django.http import HttpRequest,HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,hashers,decorators,logout
from .models import SCUser,Post,Like,ChatRoom

from django.core.urlresolvers import reverse
from forms import modifyUser, insertFile
from random import randint

# Create your views here.


"""@package docstring
     Documentation.
"""

def addLike(request):
    """Funzione di supporto che permette di aggiungere un like a un certo post
    """
    sel_post = Post.objects.get(pk=request.POST['like_post'])
    new_like = Like.objects.create(like_post=sel_post, like_user=request.user)
    new_like.save()


def deleteLike(request):
    """Funzione che permette di togliere un like
    """
    #sel_post = Post.objects.get(pk=request.POST['unlike_post'])
    print "inside delete: ",request.POST['unlike_post']
    sel_post = get_object_or_404(Post,pk=request.POST['unlike_post'])
    sel_like = Like.objects.filter(like_post=sel_post,like_user=request.user)
    sel_like.delete()


def sharePost(request):
    """Funzione che permette di condividere un post
    """
    sel_post = Post.objects.get(pk=request.POST['share'])
    p_t = sel_post.post_type
    cont = sel_post.content
    f = sel_post.file

    u = SCUser.objects.get(pk=request.user.id)
    new_post = Post.objects.create(content=cont, post_type=p_t,file=f)
    new_post.post_user.add(u)
    new_post.save()


def get_three_friends(request,scuser_id,fr):
    """Funzione che restituisce 3 amici a caso. E' utilizzata nella view profile.
    """

    #fr = SCUser.objects.filter(user=scuser_id).exclude(pk=scuser_id)[:]

    three_friends = []
    if len(fr) < 4:
        for i in xrange(len(fr)):
                three_friends.append(fr[i])
    else:
        s = set()
        while len(s) < 3:
            s.add(randint(0,len(fr)-1))
        three_friends.append(fr[s.pop()])
        three_friends.append(fr[s.pop()])
        three_friends.append(fr[s.pop()])

    return three_friends

unknow_user_list = []


def search(request):
    """Effettua la ricerca di un certo utente e restituisce una lista dei risultati.
    """
    global unknow_user_list
    unknow_user_list = []
    user_name = request.POST['res_user']
    first = user_name.split(' ')[0]
    second = user_name.split(' ')[1]
    for i in SCUser.objects.filter(first_name=first,last_name=second)[:]:
            unknow_user_list.append(i)

def create_room(user,friend,roomName):
    f = SCUser.objects.get(username=friend)
    room = ChatRoom.objects.create(name=roomName)
    room.user.add(user.id)
    room.user.add(f.id)
    room.save()

def index(request):
    """View di index che permette di effettuare il login o di accedere alla pagina di registrazione
    """
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
    """View della parte di registrazione al socialnetwork
    """
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




@decorators.login_required(login_url='/socialcircle/')
def dash(request,scuser_id):
    """Questa e' una delle view principale e gestiste l'intera interazione con la dashboard di un utente, in questa view
    un utente puo' vedere i post degli amici in ordine cronologico, cercare altre persone, inserire post(multimediali e non),
    entrare in una chat ed effettuare il logout. Questa view necessata un autenticazione obbligatoria per essere invocata.
    """
    user = get_object_or_404(SCUser,pk=scuser_id)
    if user.pk != request.user.id:
        return HttpResponseRedirect('/socialcircle/dash/%s/' %request.user.id)
    post = []
    friend = []
    global unknow_user_list


    new_fr = SCUser.objects.exclude(user=scuser_id)
    three_new_friends = get_three_friends(request,scuser_id,new_fr)

    """ricerca degli amici del proprietario della attuale dashboard
    """
    for i in SCUser.objects.filter(user=scuser_id)[:]:
        friend.append(i)

    """Selezione dei post da visualizzare sulla dashboard, in ordine cronologico, e solo degli amici dell'utente attuale.
    l'idea non e' molto efficiente si potrebbe migliorare inserendo un meccanisco di scarico parziale di nuovi post e non
    di scarico completo al refresh della pagina
    """
    #count = 0
    for k in Post.objects.filter()[:].order_by('-post_date')[:]:
        for i in k.post_user.all():
            if i in friend:# and count < 20:
                tupla = (k,SCUser.objects.get(pk=i.id))
                post.append(tupla)
                #count += 1

    post_liked = []
    for i in xrange(len(request.user.like_set.values())):
        post_liked.append(request.user.like_set.values()[i].values()[3])

    #print post

    """Gestione di tutte le richieste POST della dashboard
    """
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
            search(request)
            return HttpResponseRedirect('/socialcircle/dash/%s/#' %request.user.id)

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
        elif "chats" in request.POST:
            return HttpResponseRedirect('chat_list/')
    form = insertFile()
    data = {'scuser':user,'post':post,'post_liked' : post_liked,'unknow':unknow_user_list,
            'form':form, 'new_friends':three_new_friends}
    return render(request,'socialcircle/dashboard.html', data)





@decorators.login_required(login_url='/socialcircle/')
def profile(request,scuser_id):
    """View dedicata alla gestion del profilo utente. Anch'essa necessita di essere loggati per poterla visualizzare. Ofre
    alcune funzionalita' di gestione del profilo utente in caso siamo nella nostra pagina personale, ma anche funzionalita'
    per interaggire attivamente se siamo nel profilo di un altra persona (aggiungere agli amici, ecc...).
    """


    new_fr = SCUser.objects.exclude(user=scuser_id)
    three_new_friends = get_three_friends(request,scuser_id,new_fr)
    print three_new_friends


    global unknow_user_list
    user = get_object_or_404(SCUser,pk=scuser_id)

    friend_list = []
    for i in SCUser.objects.filter(user=request.user.id)[:]:
        friend_list.append(i.pk)


    t_fr = SCUser.objects.filter(user=scuser_id).exclude(pk=scuser_id)[:]
    three_friends= get_three_friends(request,scuser_id,t_fr)
    #TODO creare una lista con i tre amici da visualizzare nella pagina del profilo

    post_liked = []
    for i in xrange(len(request.user.like_set.values())):
        post_liked.append( request.user.like_set.values()[i].values()[3])

    post_orderd = user.post_set.order_by('-post_date')[:]

    data = {'scuser':user, 'post': post_orderd, 'post_liked' : post_liked, 'curr_user':request.user,
            'friends':friend_list,'three':three_friends, 'new_friends':three_new_friends}

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
        elif "chat" in request.POST:
            roomName = request.user.username +"-"+user.username
            room = ChatRoom.objects.filter(name=roomName)
            if len(room) == 0:
                create_room(request.user,user.username,roomName)
            return HttpResponseRedirect("/socialcircle/dash/%s/chat_list/" %request.user.id)

    elif request.method == 'GET':
        return render(request,'socialcircle/profile.html',data )



def settings(request,scuser_id):
    """View dedicata alla gestione del proprio account da parte di un utente
    """

    user = get_object_or_404(SCUser,pk=scuser_id)
    if user.pk != request.user.id:
        return HttpResponseRedirect('/socialcircle/profile/%s/settings' %request.user.id)

    password = user.password

    if request.method == 'POST':
        form = modifyUser(request.POST,request.FILES,instance=user)
        if form.is_valid():
            new_user = form.save(commit=False)
            if password != new_user.password:
                new_user.password = hashers.make_password(new_user.password,salt=None,hasher='default')
            new_user.save()
            return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )
    else:
        form = modifyUser(instance=user)
    return render(request, 'socialcircle/settings.html', {'form': form,})




def photos(request,scuser_id):
    """View che gestisce la galleria fotografica di un particolare profilo
    """

    p = True
    user = get_object_or_404(SCUser,pk=scuser_id)

    post_orderd = user.post_set.order_by('-post_date')[:]

    if "back" in request.POST:
        return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )

    return render(request,'socialcircle/gallery.html', {'fl_p':p,'scuser':user,'post':post_orderd})




def videos(request,scuser_id):
    """View che gestisce la galleria video di un particolare profilo
    """

    p = False
    user = get_object_or_404(SCUser,pk=scuser_id)

    post_orderd = user.post_set.order_by('-post_date')[:]

    if "back" in request.POST:
        return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )

    return render(request,'socialcircle/gallery.html', {'fl_p':p,'scuser':user,'post':post_orderd})


def likes(request,scuser_id):
    """View che gestisce l'elenco dei post a cui un certo utente ha messo "mi piace"
    """

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
    """View che mostra l'elenco di tutti gli attuali amici di un certo utente
    """

    user = get_object_or_404(SCUser,pk=scuser_id)
    fr = SCUser.objects.filter(user=scuser_id).exclude(pk=scuser_id)[:]
    curr_user = request.user
    if "back" in request.POST:
        return HttpResponseRedirect('/socialcircle/profile/%s' %scuser_id,{'scuser':user} )
    return render(request,'socialcircle/friends.html', {'scuser':user, 'friends':fr})


@decorators.login_required(login_url='/socialcircle/')
def chat_list(request,scuser_id):
    """View gestisce la visualizzazione delle chat attive di un certo utente e ne permette la creazione di nuovo.
    Ogni chat e' vista come una chat room a se stante a cui possono accedere 2 persone.
    """

    new_fr = SCUser.objects.exclude(user=scuser_id)
    three_new_friends = get_three_friends(request,scuser_id,new_fr)


    global unknow_user_list
    user = get_object_or_404(SCUser,pk=scuser_id)
    if user.pk != request.user.id:
        return HttpResponseRedirect('/socialcircle/dash/%s/' %request.user.id)
    #chat_rooms = ChatRoom.objects.order_by('name')[:5]
    chat_rooms = ChatRoom.objects.filter(user=scuser_id)
    context = {
        'chat_list': chat_rooms,
        'scuser':user,
        'unknow':unknow_user_list,
        'new_friends':three_new_friends,
    }
    if request.method == 'POST':
        if "res_user" in request.POST:
            search(request)
            return HttpResponseRedirect('/socialcircle/dash/%s/chat_list' %request.user.id)
        elif "newchat" in request.POST:
            friend = request.POST['newchat']
            roomName = user.username +"-"+friend
            room = ChatRoom.objects.filter(name=roomName)
            if len(room) == 0:
                create_room(user,friend,roomName)
        elif "logout" in request.POST:
            unknow_user_list = []
            logout(request)
            return HttpResponseRedirect('/socialcircle/')

    return render(request,'socialcircle/chat_list.html', context)


@decorators.login_required(login_url='/socialcircle/')
def chat_room(request,scuser_id ,chat_room_id):
    """View che gestice la vera chat room e le funzionalita'.
    """

    global unknow_user_list
    chat = get_object_or_404(ChatRoom, pk=chat_room_id)
    user = get_object_or_404(SCUser,pk=scuser_id)

    if user.id != request.user.id:
        return HttpResponseRedirect('/socialcircle/dash/%s/' %request.user.id)

    if request.method == 'POST':
        if "logout" in request.POST:
                unknow_user_list = []
                logout(request)
                return HttpResponseRedirect('/socialcircle/')
    #print "obj",chat
    return render(request, 'socialcircle/chat_room.html', {'chat': chat,'user':user})

def longpoll_chat_room(request, chat_room_id):
    chat = get_object_or_404(ChatRoom, pk=chat_room_id)
    return render(request, 'socialcircle/longpoll_chat_room.html', {'chat': chat})
