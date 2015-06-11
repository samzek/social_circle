#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^dash/(?P<scuser_id>[0-9]+)/$', views.dash, name='dash'),
        url(r'^profile/(?P<scuser_id>[0-9]+)/$', views.profile,name='profile'),
        url(r'^profile/(?P<scuser_id>[0-9]+)/settings/$', views.settings,name='settings'),
        url(r'^profile/(?P<scuser_id>[0-9]+)/photos/$', views.photos,name='photos'),
        url(r'^profile/(?P<scuser_id>[0-9]+)/videos/$', views.videos,name='videos'),
        url(r'^profile/(?P<scuser_id>[0-9]+)/likes/$', views.likes,name='likes'),
        url(r'^profile/(?P<scuser_id>[0-9]+)/friends/$', views.friends,name='friends'),
        url(r'^reg/$',views.reg,name='reg')
]

