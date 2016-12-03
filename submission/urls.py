# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submit/(?P<problem_id>\d+)/$', views.submit_page, name='submit_page'),
]
