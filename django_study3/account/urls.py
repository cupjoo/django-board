from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    # path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
]
