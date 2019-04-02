# _*_ coding: utf-8 _*_
# @time     : 2019/04/01
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm


from rest_framework import serializers
from .models import Activity


class ActivityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'title', 'status', 'start_time', 'city', 'cover')


class ActivityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        exclude =['city']