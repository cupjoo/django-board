from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.PostLV.as_view(), name='post_list'),
]
