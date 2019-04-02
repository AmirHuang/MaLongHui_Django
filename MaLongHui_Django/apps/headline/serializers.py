# _*_ coding: utf-8 _*_
# @time     : 2019/04/01
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm


from rest_framework import serializers
from headline.models import *
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['create_time', 'update_time']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'is_superuser']


class NewsSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    category = CategorySerializer(many=True)

    class Meta:
        model = News
        exclude = ['content', 'img_url', 'is_delete', 'is_show']


class NewsDetailSerializer(NewsSerializer):
    class Meta:
        model = News
        exclude = ['is_delete', 'is_show', 'img_url', 'digest']


class ComSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def validate(self, attrs):
        user_id = self.context['request'].user.id
        user = User.objects.get(id=user_id)
        if not user:
            raise serializers.ValidationError('用户不存在!')
        news = self.context['request'].data['news']
        if not news:
            raise serializers.ValidationError('要评论的新闻不存在')
        attrs['user_id'] = user_id
        return attrs

    class Meta:
        model = Comment
        fields = '__all__'
