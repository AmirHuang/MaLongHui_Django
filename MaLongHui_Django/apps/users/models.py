from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from utils.models import BaseModel


class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    residence = models.CharField(max_length=30, null=True, blank=True, verbose_name='居住地')
    schooltag = models.CharField(max_length=30, null=True, blank=True, verbose_name='毕业学校')
    company = models.CharField(max_length=30, null=True, blank=True, verbose_name='所在公司')
    website = models.CharField(max_length=30, null=True, blank=True, verbose_name='个人网站')
    avatar = models.ImageField(null=True, blank=True, verbose_name='头像')
    real_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='真人姓名')
    gender = models.CharField(max_length=10, null=True, blank=True, verbose_name='性别')
    address = models.CharField(max_length=30, null=True, blank=True, verbose_name='详细地址')
    introduce = models.CharField(max_length=50, null=True, blank=True, verbose_name='个人简介')
    wechat = models.CharField(max_length=20, null=True, blank=True, verbose_name='微信')
    qq_num = models.CharField(max_length=20, null=True, blank=True, verbose_name='QQ')
    wei_blog = models.CharField(max_length=20, null=True, blank=True, verbose_name='微博')
    photo = models.ImageField(null=True, blank=True, verbose_name='真人头像')
    # work_experience = models.ForeignKey('UserWorkExperience', related_name='users', null=True, blank=True,
    #                                     on_delete=models.SET_NULL, verbose_name='工作经历')
    # education_experience = models.ForeignKey('UserEducationExperience', related_name='users', null=True, blank=True,
    #                                          on_delete=models.SET_NULL, verbose_name='教育经历')
    birthday = models.CharField(max_length=20, null=True, blank=True, verbose_name='生日')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class UserWorkExperience(BaseModel):
    """用户工作经历表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_experiences', verbose_name='用户')
    company = models.CharField(max_length=30, null=True, blank=True, verbose_name='所在公司')
    job = models.CharField(max_length=20, null=True, blank=True, verbose_name='职位')
    start_time = models.DateField(verbose_name='开始时间')
    stop_time = models.DateField(verbose_name='结束时间')
    work_cite = models.CharField(max_length=20, null=True, blank=True, verbose_name='工作城市')
    technology = models.CharField(max_length=20, null=True, blank=True, verbose_name='相关技术')
    describe = models.CharField(max_length=30, null=True, blank=True, verbose_name='职位描述')

    class Meta:
        db_table = 'tb_user_work_experience'
        verbose_name = '工作经历'
        verbose_name_plural = verbose_name


class UserEducationExperience(BaseModel):
    """用户教育经历表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education_experiences', verbose_name='用户')
    school = models.CharField(max_length=30, null=True, blank=True, verbose_name='学校名称')
    major = models.CharField(max_length=20, null=True, blank=True, verbose_name='专业')
    start_time = models.DateField(verbose_name='开始时间')
    stop_time = models.DateField(verbose_name='结束时间')
    education_level = models.CharField(max_length=20, null=True, blank=True, verbose_name='学历')
    technology = models.CharField(max_length=20, null=True, blank=True, verbose_name='相关技术')
    achievement = models.CharField(max_length=20, null=True, blank=True, verbose_name='取得成就')

    class Meta:
        db_table = 'tb_user_education_experience'
        verbose_name = '教育'
        verbose_name_plural = verbose_name
