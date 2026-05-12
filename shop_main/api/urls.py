from . import views
from .views import *
from django.urls import path

app_name = 'api'

from django.urls import path

urlpatterns = [
        path('posts/', views.ProductListAPIView.as_view(), name='posts-list-api'),
        path('post/<int:pk>/', views.ProductDetailAPIView.as_view(), name='post-detail-api'),
        path('users/', views.UserListAPIViews.as_view(), name='user-list-api'),
        path('register/', views.UserRegistrationAPIView.as_view(), name='register_api'),
]