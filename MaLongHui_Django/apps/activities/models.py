from django.db import models


# Create your models here.

class Activity(models.Model):
    title = models.CharField(max_length=32, verbose_name="标题")
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    deadline = models.DateTimeField(verbose_name="报名截止时间")
    city = models.CharField(max_length=64, verbose_name="城市")
    address = models.CharField(max_length=64, verbose_name="地址")
    cover = models.CharField(max_length=100, verbose_name="图片")
    desc = models.TextField(verbose_name="介绍")
    detail = models.TextField(verbose_name="详情")
    sponsor = models.CharField(max_length=64, verbose_name="主办市")
    url = models.CharField(max_length=100, verbose_name="链接")
    status = models.SmallIntegerField(verbose_name="状态") # TODO 需补充Choice

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_activity'
        verbose_name = "活动"
        verbose_name_plural = verbose_name