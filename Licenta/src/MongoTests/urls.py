'''
Created on 12.03.2015

@author: Closca
'''
from django.conf.urls import patterns, url

from MongoTests import views

urlpatterns = patterns('',
    url(r'^base/$', views.base, name='base'),
    url(r'^$', views.tests, name='tests'),
)

