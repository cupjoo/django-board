from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.html'
    paginate_by = 7

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        keyword = self.request.GET.get('q')

        # 검색어 있을 시, 해당 포스트만 필터
        if keyword:
            return queryset.filter(Q(title__contains=keyword) | Q(content__contains=keyword))
        else:
            return queryset


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'board/post_create.html'
    form_class = PostForm
    login_url = None
    redirect_field_name = None

    def get_success_url(self):
        messages.info(self.request, '게시물이 작성되었습니다.')
        self.success_url = '/'
        return super(PostCreateView, self).get_success_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def test_func(self):
        pass


class PostDetailView(DetailView):
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
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(post=self.object).order_by('create_date')
        return context


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'board/post_update.html'
    form_class = PostForm

    def form_valid(self, form):
        if self.get_object().author != self.request.user:
            return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)

    def get_success_url(self):
        messages.info(self.request, '게시물이 수정되었습니다.')
        return super(PostUpdateView, self).get_success_url()


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('board:post_list')

    def delete(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return HttpResponseRedirect(self.success_url)
        return super(PostDeleteView, self).delete(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = self.delete(request, *args, **kwargs)
        messages.info(request, '게시물이 삭제되었습니다.')
        return response


def comment_delete(request, pk, c_pk):
    comment = get_object_or_404(Comment, pk=c_pk)
    success_url = reverse_lazy('board:post_detail', kwargs={'pk': pk})

    if comment.author == request.user:
        comment.delete()
    return HttpResponseRedirect(success_url)
