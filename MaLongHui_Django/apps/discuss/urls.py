# _*_ coding: utf-8 _*_
# @time     : 2019/04/01
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm

from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path(r'label_categories/', views.GetLabelCategory.as_view()),
    url(r'^label_questions/(?P<label_category_title>.*)/$', views.ListQuestion.as_view()),
    url(r'^question_details/(?P<pk>\d+)/$', views.QuestionDetail.as_view()),
    url(r'^question_comments/(?P<pk>\d+)/$', views.QuestionComment.as_view()),
    url(r'^total_labels/$', views.ShowAllLabel.as_view()),
]

