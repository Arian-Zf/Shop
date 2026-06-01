from . import views
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)

urlpatterns = [
        # path('posts/', views.ProductListAPIView.as_view(), name='posts-list-api'),
        # path('post/<int:pk>/', views.ProductDetailAPIView.as_view(), name='post-detail-api'),
        path('users/', views.UserListAPIViews.as_view(), name='user-list-api'),
        path('register/', views.UserRegistrationAPIView.as_view(), name='register_api'),
        path('', include(router.urls)),
        path('orders/', views.OrderListAPIView.as_view(), name='order-list-api'),
] 