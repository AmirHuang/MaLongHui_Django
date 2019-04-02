from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from headline.utils import NewsSetPagination


class GetNews(ListAPIView):
    pagination_class = NewsSetPagination
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_delete=False, is_show=True).all().order_by('-click')


class GetNewsDetail(RetrieveAPIView):
    serializer_class = NewsDetailSerializer
    queryset = News.objects.filter(is_show=True, is_delete=False).all()


class GetCategories(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GetCategory(ListAPIView):
    serializer_class = NewsSerializer
    pagination_class = NewsSetPagination

    def get(self, request, pk):
        self.queryset = Category.objects.get(id=pk).news_set.all()
        return super().get(self, request)


class GetComments(ListAPIView):
    serializer_class = ComSerializer

    def get(self, request, pk):
        self.queryset = News.objects.get(id=pk).comment_set.all().order_by('-update_time')
        return super().get(self, request)


class PostComments(CreateAPIView):
    serializer_class = ComSerializer
    permission_classes = [IsAuthenticated]
    pass
