# _*_ coding: utf-8 _*_
# @time     : 2019/04/01
# @Author   : Amir
# @Site     : 
# @File     : tasks.py
# @Software : PyCharm

from utils.hyt_message import Hyt_Message
import logging
from celery_tasks.main import celery_app

logger = logging.getLogger('malonghui')


@celery_app.task(name='send_sms_code')
def send_sms_code(code, mobile):
    """发送短信验证码"""
    try:
        sms = Hyt_Message()
        result = sms.send_message(code, mobile)
    except Exception as e:
        logger.error(logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e)))
    else:
        if result['code'] == 0:
            # print(result['code'], 'code')
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)

