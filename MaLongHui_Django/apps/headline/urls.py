# _*_ coding: utf-8 _*_
# @time     : 2019/04/01
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm


from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^news/$', GetNews.as_view()),  # 获取所有热门新闻数据
    url(r'^news/(?P<pk>\d+)/$', GetNewsDetail.as_view()),  # 获取新闻详情
    url(r'^cats/$', GetCategories.as_view()),  # 获取新闻分类
    url(r'^cats/(?P<pk>\d+)/$', GetCategory.as_view()),  # 获取分类下新闻
    url(r'^comments/$', PostComments.as_view()),  # 提交评论
    url(r'^comments/(?P<pk>\d+)/$', GetComments.as_view()),  # 获取分类下评论
]
