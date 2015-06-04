from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

class SCUser(models.Model):
    """
    #default : username, email, password, nome e cognome
    def __init__(self,date,address,*args,**kwargs):
        super(SCUser,self).__init__(*args,**kwargs)
        self.__date_ = date
        self.__address_ = address
    def date(self, date = None):
        if(date != None):
            self.__date_ = date
        return str(self.__date_)
    def address(self, address = None):
        if(address != None):
            self.__address_ = address
        return str(self.__address_)
    def set_name(self,first_name=None, last_name = None):
        if first_name != None:
            AbstractUser.first_name = first_name
        if last_name != None:
            AbstractUser.last_name = last_name
    def set_email (self,email):
        AbstractUser.email = email
    def set_username (self,username):
        AbstractUser.username = username

    """

    username = models.CharField(unique=True,max_length=20)

    email = models.CharField (verbose_name='email address',unique=True,max_length=255)
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True,null=False)
    is_staff = models.BooleanField(default=False,null=False)

    #profile_image = models.ImageField(upload_to="uploads",blank=False,null=False,default="path/to/file")
    user_bio = models.CharField(max_length=600,blank=True)
    password = models.CharField(max_length= 50)
    address = models.CharField(max_length=30,null=True,blank=True)
    birth_date = models.DateField()

    user = models.ManyToManyField('self',blank=True)


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

class Cat (models.Model):
    type = models.CharField(max_length=50,null=True,blank=True)
    def __unicode__(self):
        return self.type

class Post (models.Model):
    post_date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=600,null=True)
    is_photo = models.BooleanField(default=False,null=False)
    is_video = models.BooleanField(default=False,null=False)
    is_text = models.BooleanField(default=False,null=False)

    post_user = models.ManyToManyField(SCUser)
    #post_like = models.ManyToManyField(SCUser, through="Like")
    post_cat = models.ForeignKey(Cat)

    def __unicode__(self):
        return self.content


#class Pubblication (models.Model):
 #   pubb_user = models.ForeignKey(SCUser)
  #  pubb_post = models.ForeignKey(Post)
   # pubb_date = models.DateTimeField(auto_now_add=True)

   # def __unicode__(self):
    #    return self.pubb_date



class Like (models.Model):
    like_date = models.DateTimeField(auto_now_add=True)

    like_user = models.ForeignKey(SCUser)
    like_post = models.ForeignKey(Post)
    def __unicode__(self):
        return self.like_date