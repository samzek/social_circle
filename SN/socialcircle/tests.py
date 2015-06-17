from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from .models import *
from .views import *
# Create your tests here.

def create_usr1(password="Sam"):
    usr= SCUser.objects.create(username="Sam",password=password,first_name="Samuele",last_name="Zecchini",birth_date="1993-11-02",address="Roma",email="sam@gmail.com",)
    usr.password = hashers.make_password(usr.password,salt=None,hasher='default')
    usr.save()
    return usr
def create_usr2(password="Michi"):
    usr= SCUser.objects.create(username="Michi",password=password, first_name="Micaela", last_name="Verucchi", birth_date="1993-01-12", address="Milano",email="michi@gmail.com",)
    usr.password = hashers.make_password(usr.password,salt=None,hasher='default')
    usr.save()
    return usr
def create_post1():
    post= Post.objects.create(content="ciao sono triste", post_type='is_text')
    post.save()
    return post
def create_post2():
    post = Post.objects.create(content="ciao sono contento", post_type='is_text')
    post.save()
    return post


class IndexViewTests(TestCase):
    def test_index_view(self):
        client = Client()
        response = client.get(reverse('socialcircle:index'))
        self.assertEqual(response.status_code,200)

    def test_link_reg(self):
        client = Client()
        response = client.get(reverse('socialcircle:reg'))
        self.assertEqual(response.status_code,200)

    def test_login(self):
        client = Client()
        usr= create_usr1()
        response = client.get(reverse('socialcircle:dash', kwargs={'scuser_id':usr.id}))
        self.assertEqual(response.status_code,302)


class DashViewTests(TestCase):
    def test_dash_view(self): #FIXME deve fare il login
        client = Client()
        usr= create_usr1()
        response = client.get(reverse('socialcircle:dash', kwargs={'scuser_id':usr.id}))
        self.assertEqual(response.status_code,302)

    def test_dash_view_of_future_user(self):#FIXME devi fare login
        client = Client()
        response = client.get(reverse('socialcircle:dash', kwargs={'scuser_id':1}))
        self.assertEqual(response.status_code,302)

    def test_no_friends_as_new_friends(self): #FIXME fargli capire che urs1 e' autenticato altrimenti fa la ridirezione

        client = Client()
        usr1 = create_usr1()
        usr2 = create_usr2()
        usr1.user.add(usr2)

        #login_successful= self.client.login(username=usr1.username, password="Sam")
        #self.assertTrue(login_successful)

        response = client.post(reverse('socialcircle:index'), {'username': "Sam", 'password': "Sam"})
        print "res1:", response

        response = client.get(reverse('socialcircle:dash', kwargs={'scuser_id': usr1.id}))
        print "res2", response


        self.assertQuerysetEqual(response.context['new_friends'],[])

    def test_all_friends_posts_and_own_posts_in_dash(self):#FIXME fargli capire che urs1 e' autenticato altrimenti fa la ridirezione


        usr1 = create_usr1()
        post1 = create_post1()
        post1.post_user.add(usr1)

        usr2 = create_usr2()
        post2 = create_post2()
        post2.post_user.add(usr2)

        p = [post1, post2]
        client = Client()

        login_successful= self.client.login(username=usr1.username, password="Sam")
        self.assertTrue(login_successful)

        response = client.get(reverse('socialcircle:dash', kwargs={'scuser_id': usr1.id}),follow=True)
        self.assertQuerysetEqual(response.context['post'], p)

