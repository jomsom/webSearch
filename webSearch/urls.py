# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 13:06:13 2016

@author: mars
"""

from django.conf.urls import patterns, url
from websearch import views
#or from . import views

urlpatterns = [ 
    url(r'^$', views.index, name = 'index'), # when no include(), use $ at the end of regex
    url(r'^about/$', views.about, name = 'about'),
    url(r'^add_category/$', views.add_category, name = 'add_category'),
    url(r'^category/(?P<category_name_url>\w+)/$', views.category, name = 'category'),
    url(r'^register/$', views.register, name='register'), 

]
                       

#urlpatterns = [url(r'^$', views.index, name = 'index'),]