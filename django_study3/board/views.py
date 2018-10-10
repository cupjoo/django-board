from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.db.models import Q
from .models import Post
from .forms import PostForm


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


class PostCV(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'board/post_create.html'
    form_class = PostForm
    login_url = None
    redirect_field_name = None

    def get_success_url(self):
        messages.info(self.request, '게시물이 작성되었습니다.')
        return super(PostCV, self).get_success_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCV, self).form_valid(form)

    def test_func(self):
        pass
