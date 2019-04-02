# _*_ coding: utf-8 _*_
# @time     : 2019/04/01
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm


from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^spits/$', views.SpitList.as_view()),
    url(r'^spits/(?P<pk>\d+)/$', views.SpitDetail.as_view()),
    url(r'^spits_comments/(?P<pk>\d+)/$', views.SpitCommentList.as_view()),

]
