from django.views.generic import ListView
from django.db.models import Q
from .models import Post


class PostLV(ListView):
    model = Post
    template_name = 'board/post_list.html'
    paginate_by = 7

    def get_queryset(self):
        # 사용자 입력을 기다리다, get 요청이 접수되면 데이터 처리를 완료한 뒤 현재 페이지를 렌더링해 반환한다.
        queryset = super(PostLV, self).get_queryset()
        keyword = self.request.GET.get('q')

        if keyword:
            return queryset.filter(Q(title__contains=keyword) | Q(content__contains=keyword))
        else:
            return queryset
