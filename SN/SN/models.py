#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models
class SCUser (AbstractUser,models.Model):
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


if __name__ == '__main__':
    u = SCUser("24/12/1992","bondeno is my life",first_name="Samuele",last_name="Zecchini",username="samzek",email="jssdjndd@gmail.com",password="sara")
    u.set_name("maiale")
    print u.get_full_name()








