from django.db import models
from users.models import User


class Spit(models.Model):
    """吐槽"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    like_count = models.IntegerField(default=0, verbose_name="点击量")
    content = models.TextField(default='', verbose_name="吐槽内容")
    user_id = models.ForeignKey(User, related_name='user_spit', on_delete=models.CASCADE, verbose_name="用户")

    class Meta:
        db_table = 'tb_spit'
        verbose_name = '吐槽'
        verbose_name_plural = verbose_name


class SpitComment(models.Model):
    """吐槽评论"""
    user_id = models.ForeignKey(User, related_name='user_spit_comment', on_delete=models.CASCADE, verbose_name='用户')
    spit_id = models.ForeignKey(Spit, on_delete=models.CASCADE)
    content = models.CharField(max_length=32)
    like_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'tb_spit_comment'
        verbose_name = '吐槽评论'
        verbose_name_plural = verbose_name


class SpitCollection(models.Model):
    """吐槽收藏"""
    user_id = models.ForeignKey(User, related_name='user_spit_collection', on_delete=models.CASCADE, verbose_name="用户")
    spit_id = models.ForeignKey(Spit, on_delete=models.CASCADE, verbose_name="吐槽")

    class Meta:
        db_table = 'tb_spit_collection'
        verbose_name = '吐槽收藏'
        verbose_name_plural = verbose_name


class SpitLike(models.Model):
    """吐槽点赞"""
    user_id = models.ForeignKey(User, related_name='user_spit_like', on_delete=models.CASCADE, verbose_name="用户")
    spit_id = models.ForeignKey(Spit, on_delete=models.CASCADE, verbose_name="吐槽")

    class Meta:
        db_table = 'tb_spit_like'
        verbose_name = '吐槽点赞'
        verbose_name_plural = verbose_name


class CommentLike(models.Model):
    """评论点赞"""
    comment_id = models.ForeignKey(SpitComment, on_delete=models.CASCADE, verbose_name="评论id")
    user_id = models.ForeignKey(User, related_name='user_spit_comment_like', on_delete=models.CASCADE,
                                verbose_name="用户")

    class Meta:
        db_table = 'tb_spit_comment_like'
        verbose_name = '吐槽评论点赞'
        verbose_name_plural = verbose_name
