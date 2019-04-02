from django.db import models


# 头条
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True


class News(BaseModel):
    title = models.CharField(max_length=256, verbose_name="标题")
    author = models.ForeignKey('users.User', default=None, verbose_name='作者', on_delete=models.CASCADE)
    source = models.CharField(max_length=64, default=None, verbose_name='来源')
    category = models.ManyToManyField('Category', verbose_name='分类')
    content = models.TextField(verbose_name="内容")
    is_delete = models.NullBooleanField(default=False, verbose_name="是否逻辑删除")
    is_show = models.NullBooleanField(default=False, verbose_name="是否过审")
    img_url = models.CharField(max_length=256, verbose_name="链接")
    click = models.IntegerField(default=0, verbose_name='点击量')
    digest = models.CharField(default='', max_length=512, verbose_name='详情描述')

    class Meta:
        db_table = 'tb_news'
        verbose_name = "头条"
        verbose_name_plural = verbose_name


class Category(BaseModel):
    name = models.CharField(max_length=32, verbose_name="分类")

    class Meta:
        db_table = 'tb_category'
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Comment(BaseModel):
    user = models.ForeignKey('users.User', verbose_name='用户ID', on_delete=models.CASCADE)
    news = models.ForeignKey('News', verbose_name='新闻ID', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='评论内容')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="此评论的父评论")

    class Meta:
        db_table = 'tb_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
