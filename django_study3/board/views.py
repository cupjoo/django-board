from django.views.generic import ListView
from django.db.models import Q
from .models import Post


class PostLV(ListView):
    model = Post
    template_name = 'board/post_list.html'
    paginate_by = 7

    def get_queryset(self):
        queryset = super(PostLV, self).get_queryset()
        keyword = self.request.GET.get('q')

        if keyword:
            return queryset.filter(Q(title__contains=keyword) | Q(content__contains=keyword))
        else:
            return queryset
