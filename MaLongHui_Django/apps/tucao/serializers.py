# _*_ coding: utf-8 _*_
# @time     : 2019/04/01
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm


from rest_framework import serializers
from .models import *
from users.serializers import UserDetailSerializer


class SpitSerializer(serializers.ModelSerializer):
    """吐槽列表序列化器"""

    # user_id = UserDetailSerializer()
    class Meta:
        model = Spit
        fields = '__all__'

    # """吐槽列表序列化器"""
    # user_id = UserDetailSerializer(read_only=True)
    #
    # class Meta:
    #     model = Spit
    #     fields = ('id', 'content', 'create_time', 'like_count', 'user_id')
    def create(self, validated_data):
        spit = super(SpitSerializer, self).create(validated_data)
        return spit


class SpitCommentSerializer(serializers.ModelSerializer):
    # 吐槽评论序列化器

    class Meta:
        model = SpitComment
        fields = '__all__'


class SpitDetailSerializer(serializers.ModelSerializer):
    # user_id = UserDetailSerializer()

    class Meta:
        model = Spit
        fields = '__all__'
