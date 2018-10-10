from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('board.urls', namespace='board')),
    path('summernote/', include('django_summernote.urls')),
]
