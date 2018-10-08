from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_display_links = ['id', 'title']
    list_filter = ['author']
    list_editable = ['author']
    fields = ('title', 'author', 'content')


admin.site.register(Post)
