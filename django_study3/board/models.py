from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields


class Post(summer_model.Attachment):
    POST_TYPE = (
        (0, '공지사항'),
        (1, '자유게시판'),
    )
    title = models.CharField('title', max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = summer_fields.SummernoteTextField(default='')
    create_date = models.DateTimeField('Create Date', auto_now_add=True)
    modify_date = models.DateTimeField('Modify Date', auto_now=True)
    type = models.PositiveSmallIntegerField('type', choices=POST_TYPE)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('board:post_detail', kwargs={'pk': self.id})

    def get_prev(self):
        return self.get_previous_by_create_date()

    def get_next(self):
        return self.get_next_by_create_date()


class Comment(models.Model):
    post = models.ForeignKey('board.Post', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField('content')
    create_date = models.DateTimeField('created date', auto_now_add=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ['-create_date']

    def __str__(self):
        return self.content
