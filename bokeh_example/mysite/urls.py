# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 16:22:11 2019

@author: James Beaudoin
"""

from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
 path("", views.homepage, name="homepage"),
 path("home", views.storytelling, name="dashboard"),
 path("about", views.about, name="about"),
 path("contact", views.contact, name="contact"),
 path("howitworks", views.howitworks, name="howitworks"),
 path("yourstory", views.dashboard, name="storytelling"),

]
