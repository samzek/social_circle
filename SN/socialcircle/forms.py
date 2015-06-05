#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import ModelForm
from models import SCUser

class modifyUser(ModelForm):
    class Meta:
        model = SCUser
        fields = ['first_name','last_name','username','email','birth_date','password','address','user_bio']