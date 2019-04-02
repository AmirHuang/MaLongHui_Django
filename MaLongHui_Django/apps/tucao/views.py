from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

# Create your views here.

from .serializers import *
from .utils import SpitSetPagination


class SpitList(ListAPIView, CreateAPIView):
    # 吐槽列表
    # serializer_class = SpitSerializer
    #
    # def get_queryset(self):
    #     return Spit.objects.all().order_by('-id')
    pagination_class = SpitSetPagination
    queryset = Spit.objects.all().order_by('-id')
    serializer_class = SpitSerializer


class SpitDetail(RetrieveAPIView):
    # 吐槽详情
    # serializer_class = SpitDetailSerializer
    #
    # def get(self, request, pk):
    #     self.queryset = News.objects.filter(is_show=True, is_delete=False, id=pk).all()
    #     return super().get(self, request)
    serializer_class = SpitDetailSerializer
    queryset = Spit.objects.all()


class SpitCommentList(ListAPIView, CreateAPIView):
    serializer_class = SpitCommentSerializer

    def get(self, request, pk):
        self.queryset = Spit.objects.get(id=pk).spitcomment_set.all()
        return super().get(self, request)
