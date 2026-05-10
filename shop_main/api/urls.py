from . import views
from django.urls import path

app_name = 'api'

from django.urls import path

urlpatterns = [
        path('posts/', views.PostListAPIView.as_view(), name='posts-list-api'),
        path('post/<int:pk>/', views.PostDetailAPIView.as_view(), name='post-detail-api'),
]