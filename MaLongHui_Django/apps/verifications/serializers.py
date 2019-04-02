# _*_ coding: utf-8 _*_
# @time     : 2019/03/30
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

import re
from django_redis import get_redis_connection
from rest_framework import serializers

from users.models import User


class SMSCheckSerializer(serializers.ModelSerializer):
    """
    短信验证码校验序列化器
    """

    class Meta:
        model = User
        # fields = ('mobile', 'username')
        fields = ('mobile',)

    def validate_mobile(self, mobile):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise serializers.ValidationError('手机号格式错误')
        user = None
        try:
            user = User.objects.get(mobile=mobile)
        except Exception:
            pass
        if user:
            raise serializers.ValidationError('手机号已申请')
        return mobile

    # def validate_username(self, username):
    #     """验证昵称用户名"""
    #     user = None
    #     try:
    #         user = User.objects.get(username=username)
    #     except Exception:
    #         pass
    #     if user:
    #         raise serializers.ValidationError('用户名已被占用')
    #     return username

    # def validate(self, attrs):
    #     mobile = self.validated_data['mobile']
    #     redis_conn = get_redis_connection('verify_code')
    #     send_flag = redis_conn.get('send_flag_%s' % mobile)
    #     if send_flag:
    #         raise serializers.ValidationError('请求次数过于频繁')
    #     return attrs

    def validate(self, attrs):
        mobile = self.context['view'].kwargs['mobile']
        redis_conn = get_redis_connection('verify_code')
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            raise serializers.ValidationError('请求次数过于频繁')

        return attrs
