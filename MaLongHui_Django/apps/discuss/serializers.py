# _*_ coding: utf-8 _*_
# @time     : 2019/04/01
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

from rest_framework import serializers

from users.models import User
from . import models


class ListLabelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LabelCategory
        fields = ('id', 'title')


class BelongUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ListQuestionSerializer(serializers.ModelSerializer):
    # answer_user_id = serializers.CharField(label='回答用户', read_only=True)
    # last_answer_time = serializers.DateTimeField(label='最新评论时间', required=False)
    belong_user = BelongUserSerializer()
    belong_label = ListLabelCategorySerializer(many=True)

    class Meta:
        model = models.Question
        fields = ('id', 'title', 'clicks', 'answer_counts', 'like_counts', 'create_time',
                  'belong_user', 'belong_label')


class QuestionDetailSerializer(serializers.ModelSerializer):
    belong_user = BelongUserSerializer()
    belong_label = ListLabelCategorySerializer(many=True)

    class Meta:
        model = models.Question
        fields = (
            'id', 'title', 'content', 'like_counts', 'belong_user', 'belong_label', 'create_time', 'answer_counts')


class QuestionCommentSerializer(serializers.ModelSerializer):
    belong_user = BelongUserSerializer()

    class Meta:
        model = models.QuestionComment
        fields = ('id', 'comment_content', 'like_counts', 'belong_user')


class ShowAllLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LabelCategory
        fields = ('id', 'title', 'like_counts')
