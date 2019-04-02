# _*_ coding: utf-8 _*_
# @time     : 2019/04/01
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm

from django.urls import path
from . import views


urlpatterns = [
    # path('sms_codes/<str:mobile>/', views.SMSCodeView.as_view()),
    path('sms_codes/<str:mobile>/', views.SmsCode.as_view()),
]
