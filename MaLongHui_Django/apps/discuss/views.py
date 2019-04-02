from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import LabelCategory, Question
from .serializers import ListLabelCategorySerializer, ListQuestionSerializer, QuestionDetailSerializer, \
    QuestionCommentSerializer, ShowAllLabelSerializer
from .utils import StandardPageNumberPagination
import logging

logger = logging.getLogger('malonghui')


# url(r'^label_categories/$', views.GetLabelCategory.as_view()),
class GetLabelCategory(APIView):
    def get(self, request):
        data = LabelCategory.objects.all().order_by('-like_counts')[0:4]
        serializer = ListLabelCategorySerializer(data, many=True)
        return Response(serializer.data)


# url(r'^label_questions/(?P<label_category_title>.*)/$', views.ListQuestion.as_view()),
class ListQuestion(GenericAPIView):
    serializer_class = ListQuestionSerializer
    pagination_class = StandardPageNumberPagination

    def get_queryset(self):
        return None

    def add_attr(self, questions):
        for question in questions:
            question.belong_user = question.source
            question.belong_label = question.label
        serializer = self.get_serializer(questions, many=True)
        return serializer

    def get(self, request, label_category_title):
        """
        根据前端匹配的url和查询的字符串返还相应的问题数据
        :param request:
        :param label_category_title:
        :return:
        """

        try:
            category = request.query_params.get('category')
        except Exception as e:
            logger.error(e)
            return Response({'message': '参数错误'})

        if label_category_title == 'index':
            """没有语言标签，获取的是首页数据"""
            if category == 'newest':
                """最新回答数据"""
                questions = Question.objects.all().order_by('-create_time')

                return Response(self.add_attr(questions).data)

            elif category == 'hot':
                """热门回答数据"""
                questions = Question.objects.all().order_by('-clicks')

                return Response(self.add_attr(questions).data)

            elif category == 'waited':
                """等待回答数据"""
                questions = Question.objects.filter(answer_counts=0).order_by('create_time')

                return Response(self.add_attr(questions).data)

            else:
                return Response({'message': '参数错误'})

        else:
            """有选中语言标签，获取的是对应的语言标签数据"""
            label_categorys = LabelCategory.objects.all()
            label_list = []
            for label_category in label_categorys:
                label_list.append(label_category.title)

            if label_category_title not in label_list:
                return Response({'message': '参数错误'})

            label = LabelCategory.objects.get(title=label_category_title)

            if category == 'newest':
                """最新回答数据"""
                questions = Question.objects.filter(label=label).order_by('-create_time')

                return Response(self.add_attr(questions).data)

            elif category == 'hot':
                """热门回答数据"""
                questions = Question.objects.filter(label=label).order_by('-clicks')

                return Response(self.add_attr(questions).data)

            elif category == 'waited':
                """等待回答数据"""
                questions = Question.objects.filter(Q(label=label) | Q(answer_counts=0)).order_by('create_time')

                return Response(self.add_attr(questions).data)
            else:
                return Response({'message': '参数错误'})


# url(r'^question_details/(?P<pk>\d+)/$', views.QuestionDetail.as_view())
class QuestionDetail(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        q = Question.objects.get(id=pk)
        q.clicks += 1
        q.save()
        instance = self.get_object()
        instance.belong_user = instance.source
        instance.belong_label = instance.label
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# url(r'^question_comments/(?P<pk>\d+)/$)', views.QuestionComment.as_view()),
class QuestionComment(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        q = Question.objects.get(id=pk)
        comments = q.questioncomment_set.all()
        for comment in comments:
            comment.belong_user = comment.source
        serializer = QuestionCommentSerializer(comments, many=True)
        return Response(serializer.data)


# url(r'^total_labels/$', views.ShowAllLabel.as_view()),
class ShowAllLabel(ListAPIView):
    queryset = LabelCategory.objects.all()
    serializer_class = ShowAllLabelSerializer
