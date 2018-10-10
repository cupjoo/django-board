from django.urls import path
from .views import *

app_name = 'board'
urlpatterns = [
    path('', PostLV.as_view(), name='post_list'),
]
