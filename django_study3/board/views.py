from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.contrib import messages
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm


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
        self.success_url = '/'
        return super(PostCV, self).get_success_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCV, self).form_valid(form)

    def test_func(self):
        pass


class PostDV(DetailView):
    template_name = 'board/post_detail.html'
    model = Post
    form = CommentForm

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        author = request.user
        content = request.POST.get('content')
        Comment.objects.create(post=post,author=author, content=content)
        messages.info(request, '댓글이 작성되었습니다.')
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form'] = self.form
        context = super(PostDV, self).get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(post=self.object).order_by('create_date')
        return context
