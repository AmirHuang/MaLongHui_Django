from django.db import models
from utils.models import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField
from users.models import User


class LabelCategory(models.Model):
    title = models.CharField(max_length=32, verbose_name='语言标签')
    like_counts = models.IntegerField(default=0, verbose_name='关注数')
    content = models.CharField(max_length=512, verbose_name='语言标签简介', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='labs', null=True, blank=True,
                               verbose_name='所属父级语言标签')
    user_like = models.ManyToManyField(to=User, db_table='tb_user_like_label', verbose_name='用户关注')

    class Meta:
        db_table = 'tb_label_category'
        verbose_name = '语言标签分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Question(BaseModel):
    title = models.CharField(max_length=256, verbose_name='标题')
    content = RichTextUploadingField(default='', verbose_name='问题详细信息')
    clicks = models.IntegerField(default=0, verbose_name='浏览量')
    # status = models.BooleanField(default=False, verbose_name='问题解决状态')
    answer_counts = models.IntegerField(default=0, verbose_name='评论量')
    like_counts = models.IntegerField(default=0, verbose_name='问题点赞量')
    source = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='问题发布的用户')
    label = models.ManyToManyField(to=LabelCategory, db_table='tb_label_question', verbose_name='问题所属标签')
    user_like = models.ManyToManyField(to=User, db_table='tb_user_like_question', related_name='like_questions',
                                       verbose_name='问题点赞的用户')

    class Meta:
        db_table = 'tb_question'
        verbose_name = '问题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '标题: %s *** 发布者: %s' % (self.title, self.source.username)


class QuestionComment(BaseModel):
    comment_content = RichTextUploadingField(default='', verbose_name='评论详细信息')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='details', null=True, blank=True,
                               verbose_name='所属父级评论')
    question = models.ForeignKey(Question, on_delete=models.PROTECT, verbose_name='评论所属问题')
    like_counts = models.IntegerField(default=0, verbose_name='点赞数')
    source = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='评论发布的用户')
    user_like = models.ManyToManyField(to=User, db_table='tb_user_like_comment', related_name='like_comment',
                                       verbose_name='评论点赞的用户')

    class Meta:
        db_table = 'tb_question_comment'
        verbose_name = '评论表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '评论所属问题: %s *** 评论发布者: %s' % (self.question.title, self.source.username)