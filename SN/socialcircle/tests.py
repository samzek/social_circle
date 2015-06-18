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
    def test_dash_view(self):
        client = Client()
        usr= create_usr1()

        response = client.post(reverse('socialcircle:index'),{'username':usr.username,'password':"Sam",'log_in':"log_in"})
        response = client.get(reverse('socialcircle:dash', kwargs={'scuser_id':usr.id}))

        self.assertEqual(response.status_code,200)

    def test_dash_view_of_future_user(self):
        client = Client()
        usr= create_usr1()

        response = client.post(reverse('socialcircle:index'),{'username':usr.username,'password':"Sam",'log_in':"log_in"})
        response = client.get(reverse('socialcircle:dash', kwargs={'scuser_id':2}))

        self.assertEqual(response.status_code,404)

    def test_redirect_if_url_manually_changed(self):
        client = Client()
        usr1= create_usr1()
        usr2 = create_usr2()

        response = client.post(reverse('socialcircle:index'),{'username':usr1.username,'password':"Sam",'log_in':"log_in"})
        response = client.get(reverse('socialcircle:dash', kwargs={'scuser_id':usr2.id}))

        self.assertEqual(response.status_code,302)

    def test_no_friends_as_new_friends(self):

        client = Client()
        usr1 = create_usr1()
        usr2 = create_usr2()
        usr1.user.add(usr2)
        usr1.user.add(usr1)

        response = client.post(reverse('socialcircle:index'),{'username':usr1.username,'password':"Sam",'log_in':"log_in"})
        response = client.get(reverse('socialcircle:dash', kwargs={'scuser_id': usr1.id}),follow=True)

        self.assertQuerysetEqual(response.context['new_friends'],[])

    def test_all_friends_posts_and_own_posts_in_dash(self):

        usr1 = create_usr1()
        post1 = create_post1()
        post1.post_user.add(usr1)

        usr2 = create_usr2()
        post2 = create_post2()
        post2.post_user.add(usr2)

        usr1.user.add(usr2)
        usr1.user.add(usr1)

        p = [(post2,usr2),(post1,usr1)]
        client = Client()

        response = client.post(reverse('socialcircle:index'),{'username':usr1.username,'password':"Sam",'log_in':"log_in"})
        response = client.get(reverse('socialcircle:dash', kwargs={'scuser_id': usr1.id}))

        self.assertEqual(response.context['post'], p)

    def test_unknown_list_empty_on_login(self):
        client = Client()
        usr1 = create_usr1()
        usr2 = create_usr2()
        usr1.user.add(usr2)

        response = client.post(reverse('socialcircle:index'),{'username':usr1.username,'password':"Sam",'log_in':"log_in"})
        #print "status_login:",response.status_code

        response = client.get(reverse('socialcircle:dash', kwargs={'scuser_id': usr1.id}),follow=True)

        self.assertQuerysetEqual(response.context['unknow'],[])

    def test_unknown_list_empty_on_logout(self):

        client = Client()
        usr1 = create_usr1()
        usr2 = create_usr2()
        usr1.user.add(usr2)

        response = client.post(reverse('socialcircle:index'),{'username':usr1.username,'password':"Sam",'log_in':"log_in"})
        response_1 = client.get(reverse('socialcircle:dash', kwargs={'scuser_id': usr1.id}),follow=True)
        response = client.post(reverse('socialcircle:dash',kwargs={'scuser_id':usr1.id}),{'logout':"logout"})

        self.assertEqual(response.status_code,302)
        self.assertQuerysetEqual(response_1.context['unknow'],[])

    def test_redirect_profile(self):
        client = Client()
        usr1 = create_usr1()
        usr2 = create_usr2()
        usr1.user.add(usr2)

        response_1 = client.post(reverse('socialcircle:index'),{'username':usr1.username,'password':"Sam",'log_in':"log_in"})
        response_2 = client.get(reverse('socialcircle:dash', kwargs={'scuser_id': usr1.id}),follow=True)
        response = client.post(reverse('socialcircle:dash',kwargs={'scuser_id':usr1.id}),{'profile':"profile"})

        self.assertEqual(response.status_code,302)

    def test_redirect_chat(self):
        client = Client()
        usr1 = create_usr1()
        usr2 = create_usr2()
        usr1.user.add(usr2)

        response_1 = client.post(reverse('socialcircle:index'),{'username':usr1.username,'password':"Sam",'log_in':"log_in"})
        response_2 = client.get(reverse('socialcircle:dash', kwargs={'scuser_id': usr1.id}),follow=True)
        response = client.post(reverse('socialcircle:dash',kwargs={'scuser_id':usr1.id}),{'chat':"chat"})

        self.assertEqual(response.status_code,200)

    def test_submit_a_post_with_test(self):
        client = Client()
        usr1 = create_usr1()
        usr2 = create_usr2()
        usr1.user.add(usr2)
        usr1.user.add(usr1)

        response_1 = client.post(reverse('socialcircle:index'),{'username':usr1.username,'password':"Sam",'log_in':"log_in"})
        response_2 = client.get(reverse('socialcircle:dash', kwargs={'scuser_id': usr1.id}),follow=True)
        response = client.post(reverse('socialcircle:dash',kwargs={'scuser_id':usr1.id}),{'submit_text':"submit_text",
                                                                                          'text_post':"prova test"},follow=True)
        self.assertTrue(response.context['post'])

    def test_submit_a_video(self):
        client = Client()
        usr1 = create_usr1()
        usr2 = create_usr2()
        usr1.user.add(usr2)
        usr1.user.add(usr1)

        response_1 = client.post(reverse('socialcircle:index'),{'username':usr1.username,'password':"Sam",'log_in':"log_in"})
        response_2 = client.get(reverse('socialcircle:dash', kwargs={'scuser_id': usr1.id}),follow=True)
        response = client.post(reverse('socialcircle:dash',kwargs={'scuser_id':usr1.id}),{'submit_video':"submit_video"}
                               ,follow=True)

        self.assertTrue(response.context['form'].is_valid)
        self.assertTrue(response.context['post'])

    def test_if_there_are_likes(self):
        client = Client()
        usr1 = create_usr1()
        usr2 = create_usr2()
        usr1.user.add(usr2)

        post2 = create_post2()
        post2.post_user.add(usr2)

        new_like = Like.objects.create(like_post=post2, like_user=usr1)
        new_like.save()

        response_1 = client.post(reverse('socialcircle:index'),{'username':usr1.username,'password':"Sam",'log_in':"log_in"})
        response_2 = client.get(reverse('socialcircle:dash', kwargs={'scuser_id': usr1.id}),follow=True)

        self.assertGreater(len(response_2.context['post_liked']),0)



