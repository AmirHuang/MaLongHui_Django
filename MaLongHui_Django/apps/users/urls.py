# _*_ coding: utf-8 _*_
# @time     : 2019/03/30
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm

from django.urls import path
from rest_framework import routers

from . import views
from rest_framework_jwt.views import obtain_jwt_token

routers = routers.DefaultRouter()
routers.register(r'work_experiences', views.UserWorkExperienceViewSet, base_name='work_experiences')
routers.register(r'education_experiences', views.UserEducationExperienceViewSet, base_name='education_experiences')

urlpatterns = [
    path(r'user/', views.UserDetailView.as_view()),
    path(r'usernames/<str:username>/count/', views.UsernameCountView.as_view()),
    path(r'mobiles/<str:mobile>/count/', views.MobileCountView.as_view()),
    path(r'users/', views.UserView.as_view()),
    path(r'authorizations/', obtain_jwt_token),
]
urlpatterns += routers.urls