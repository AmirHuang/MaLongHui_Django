# _*_ coding: utf-8 _*_
# @time     : 2019/04/01
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm

from django.urls import path
from . import views

urlpatterns = [
    path(r'activities/', views.ActivityListView.as_view()),
    path(r'activities/<int:pk>/', views.ActivityDetailView.as_view()),

]

