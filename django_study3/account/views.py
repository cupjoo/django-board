from django.contrib.auth import views, logout
from django.contrib import messages
from django.views.generic import RedirectView, CreateView
from django.urls import reverse_lazy
from .forms import UserCreationForm, InfoChangeForm


class LoginView(views.LoginView):
    template_name = 'account/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        # 로그인 성공후 이전 페이지로 리다이렉션 시킴
        # 최초 페이지 반환 시 next 인자에 경로를 지정시켜줌
        context['next'] = self.request.META.get('HTTP_REFERER', '/')

        return context

    def form_valid(self, form):
        messages.info(self.request, "로그인되었습니다.")
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    # 로그아웃 템플릿 없이 로그아웃만 진행함
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "로그아웃되었습니다.")
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        messages.info(self.request, "회원가입되었습니다.")
        return super(SignupView, self).form_valid(form)


# 브라우저 종료 시 자동 로그아웃 구현
# 클래스 오버라이딩
class InfoChangeView(views.PasswordChangeView):
    form_class = InfoChangeForm
    success_url = '/'
    template_name = 'account/info_change.html'

    def form_valid(self, form):
        messages.info(self.request, "개인정보가 변경되었습니다.")
        return super(InfoChangeView, self).form_valid(form)
