import random

from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from celery_tasks.sms.tasks import send_sms_code
from rest_framework.views import  APIView

from .serializers import SMSCheckSerializer


# url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
class SMSCodeView(GenericAPIView):
    """
    短信验证码
    传入参数：
        mobile, username,
    """
    serializer_class = SMSCheckSerializer

    def get(self, request, mobile):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        sms_code = '%06d' % random.randint(0, 999999)
        print('>>%s<<' % sms_code)

        redis_conn = get_redis_connection('verify_code')
        p1 = redis_conn.pipeline()
        p1.setex('sms_%s' % mobile, 300, sms_code)
        p1.setex('send_flag_%s' % mobile, 60, 1)
        p1.execute()

        # 使用异步发送短信
        # expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        # send_sms_code.delay(mobile, sms_code, expires, constants.SMS_CODE_TEMP_ID)
        result_dic = send_sms_code(sms_code, mobile)
        return Response(result_dic)


class SmsCode(APIView):

    def get(self, request, mobile):
        # 1.从前端获取手机号
        # 2.对手机号进行正则校验
        # 3.生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # print(sms_code)
        # 4.保存短信信息到ｒｅｄｉｓ数据中
        # 和redis数据库建立连接
        con = get_redis_connection('verify_code')
        flag = con.get('send_flag_%s' % mobile)
        # print('----flag', flag)
        if flag:
            return Response({'error': '请求过于频繁'})
        # 生成管道对象
        p1 = con.pipeline()
        # 保存短信验证码到redis中
        p1.setex('sms_%s' % mobile, 300, sms_code)
        # 设置请求时效标志
        p1.setex('send_flag_%s' % mobile, 60, 1)
        # 执行管道（连接缓存， 存入数据）
        p1.execute()
        # 使用celery异步发送短信
        send_sms_code(sms_code, mobile)
        return Response({"message":"ok"})
