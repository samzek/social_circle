from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

class SCUser(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(unique=True,max_length=20)

    email = models.CharField (verbose_name='email address',unique=True,max_length=255)
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True,null=False)
    is_admin    = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False,null=False)

    profile_image = models.ImageField(upload_to="media/avatar/",blank=False,null=False,default="media/avatar/unknow_user.jpg")
    user_bio = models.CharField(max_length=600,blank=True)
    address = models.CharField(max_length=30,null=True,blank=True)
    birth_date = models.DateField(null=False)

    user = models.ManyToManyField('self',blank=True)

    REQUIRED_FIELDS = ['email','first_name','last_name','birth_date']
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.username

    def date(self, date = None):
        if(date != None):
            self.birth_date = date
        return str(self.__date_)
    def get_set_address(self, address = None):
        if(address != None):
            self.address = address
        return str(self.__address_)
    def set_name(self,first_name=None, last_name = None):
        if first_name != None:
            self.first_name = first_name
        if last_name != None:
            self.last_name = last_name
    def set_email (self,email):
        self.email = email
    def set_username (self,username):
        self.username = username

class Post (models.Model):
    post_date = models.DateTimeField(auto_now_add=True)

    TEXT= 'is_text'
    VIDEO = 'is_video'
    PHOTO = 'is_photo'

    POST_CHOICES = (
        (TEXT, 'Text'),
        (VIDEO, 'Video'),
        (PHOTO, 'Photo'),
    )
    post_type = models.CharField(max_length=20, choices=POST_CHOICES,default=TEXT)

    content = models.CharField(max_length=600,null=True,blank=True,default="")
    file = models.FileField(upload_to='media/%Y/%m/%d', blank=True)

    post_user = models.ManyToManyField(SCUser)

    def __unicode__(self):
        return 'Post ID: '+ str(self.id)


class Like (models.Model):
    like_date = models.DateTimeField(auto_now_add=True)

    like_user = models.ForeignKey(SCUser)
    like_post = models.ForeignKey(Post)
    def __unicode__(self):
        return unicode(self.like_date) + " | "+ self.like_user.username

class ChatRoom(models.Model):
    name = models.CharField(max_length=200)
    user = models.ManyToManyField(SCUser)

    def __unicode__(self):
        return self.name
