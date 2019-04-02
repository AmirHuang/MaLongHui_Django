from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication

from .models import User
from users import serializers


# /user/
class UserDetailView(RetrieveUpdateAPIView):
    """用户基本信息"""
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # 返回当前请求的用户
        # 在类视图对象中，可以通过类视图对象的属性获取request
        # 在django的请求request对象中，user属性表明当请请求的用户
        return self.request.user

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = serializers.UpdateUserDetailSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


# # /user/
# class UserDetailView(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
#     """用户基本信息"""
#     permission_classes = [IsAuthenticated]
#
#     def get_serializer_class(self):
#         if self.action == 'update':
#             return serializers.UpdateUserDetailSerializer
#         else:
#             return serializers.UserDetailSerializer
#
#     def get_object(self):
#         # 返回当前请求的用户
#         # 在类视图对象中，可以通过类视图对象的属性获取request
#         # 在django的请求request对象中，user属性表明当请请求的用户
#         return self.request.user


# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
class UsernameCountView(APIView):
    """
    用户名数量
    """

    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }
        return Response(data)


# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class MobileCountView(APIView):
    """
    手机号数量
    """

    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)


# url(r'^users/$', views.UserView.as_view()),
class UserView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = serializers.CreateUserSerializer


class UserWorkExperienceViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                RetrieveUpdateAPIView,GenericViewSet):
    serializer_class = serializers.UserWorkExperienceSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.work_experiences

    def list(self, request, *args, **kwargs):
        """用户工作经历列表视图"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'work_experience': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """添加用户工作经历视图"""
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """更新用户工作经历视图"""
        return super().update(request, *args, **kwargs)

# class UserWorkExperienceViewSet(mixins.UpdateModelMixin,
#                                 mixins.CreateModelMixin,
#                                 mixins.ListModelMixin,
#                                 mixins.RetrieveModelMixin,
#                                 GenericViewSet):
#     serializer_class = serializers.UserWorkExperienceSerializer
#     permissions = [IsAuthenticated]
#
#     def get_queryset(self):
#         return self.request.user.work_experiences
#
#     def list(self, request, *args, **kwargs):
#         """用户工作经历列表视图"""
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         user = self.request.user
#         return Response({
#             'user_id': user.id,
#             'work_experience': serializer.data
#         })
#
#     # def list(self, request, *args, **kwargs):
#     #     queryset = self.filter_queryset(self.get_queryset())
#     #     user = self.request.user
#     #     page = self.paginate_queryset(queryset)
#     #     if page is not None:
#     #         serializer = self.get_serializer(page, many=True)
#     #         return self.get_paginated_response({
#     #             'user_id': user.id,
#     #             'work_experience': serializer.data
#     #         })
#     #
#     #     serializer = self.get_serializer(queryset, many=True)
#     #     return Response({
#     #         'user_id': user.id,
#     #         'work_experience': serializer.data
#     #     })


class UserEducationExperienceViewSet(mixins.RetrieveModelMixin,
                                     mixins.UpdateModelMixin,
                                     mixins.CreateModelMixin,
                                     mixins.ListModelMixin,
                                     GenericViewSet):
    serializer_class = serializers.UserEducationExperienceSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.education_experiences

    def list(self, request, *args, **kwargs):
        """用户教育经历列表视图"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'education_experience': serializer.data
        })

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     user = self.request.user
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response({
    #             'user_id': user.id,
    #             'education_experience': serializer.data
    #         })
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response({
    #         'user_id': user.id,
    #         'education_experience': serializer.data
    #     })
