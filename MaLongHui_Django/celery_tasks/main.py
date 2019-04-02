# _*_ coding: utf-8 _*_
# @time     : 2019/04/01
# @Author   : Amir
# @Site     : 
# @File     : main.py
# @Software : PyCharm

from celery import Celery

# 为celery使用django配置文件进行设置
import os

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'MaLongHui_Django.settings'

# 创建celery应用
celery_app = Celery('malonghui_django')

# 导入celery配置
celery_app.config_from_object('celery_tasks.config')

# 导入任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])

# celery -A celery_tasks.main worker -l info