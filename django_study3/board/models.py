from django.conf import settings
from django.db import models
from django.urls import reverse
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields


class Post(summer_model.Attachment):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = summer_fields.SummernoteTextField(default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('board:post_detail', args=[self.id])

    def __str__(self):
        return self.title
