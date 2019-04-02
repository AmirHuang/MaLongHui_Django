# _*_ coding: utf-8 _*_
# @time     : 2019/03/30
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

import re
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.serializers import api_settings

from users.models import User, UserWorkExperience, UserEducationExperience


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    """

    class Meta:
        model = User
        fields = (
            'username', 'avatar', 'introduce', 'residence', 'schooltag', 'company', 'website', 'real_name', 'gender',
            'mobile', 'email', 'address', 'birthday')


class CreateUserSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'sms_code', 'allow', 'mobile', 'token')
        extra_kwargs = {
            'username': {
                'min_length': 4,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 6,
                'max_length': 16,
                'error_messages': {
                    'min_length': '仅允许6-16个字符的密码',
                    'max_length': '仅允许6-16个字符的密码'
                }
            }
        }

    def validate_mobile(self, mobile):
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise serializers.ValidationError('手机号格式错误')
        return mobile

    def validate_allow(self, allow):
        if allow != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return allow

    def validate(self, attrs):
        """验证短信验证码"""
        redis_conn = get_redis_connection('verify_code')
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if not real_sms_code:
            raise serializers.ValidationError('无效的短信验证码')
        if attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')
        return attrs

    def create(self, validated_data):
        del validated_data['sms_code']
        del validated_data['allow']

        user = super().create(validated_data)
        # print('加密之前的密码：', user.password)
        user.set_password(validated_data['password'])
        user.save()

        # 生成记录登录状态的jwt_token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user


class UpdateUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'avatar', 'introduce', 'residence', 'schooltag', 'company', 'website', 'real_name', 'gender', 'mobile',
            'email', 'address', 'birthday', 'email')


class UserWorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkExperience
        user = UserDetailSerializer
        fields = '__all__'


class UserEducationExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducationExperience
        user = UserDetailSerializer
        fields = '__all__'





