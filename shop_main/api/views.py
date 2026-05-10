from django.shortcuts import render
from shop.models import Product
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from account.models import ShopUser
from rest_framework.response import Response
from rest_framework .permissions import AllowAny


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserListAPIViews(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        users = ShopUser.objects.all()
        serializer = ShopUserSerializer(users, many=True)
        return Response(serializer.data)
