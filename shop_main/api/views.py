from django.shortcuts import render
from shop.models import Product
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from account.models import ShopUser
from rest_framework.response import Response
from rest_framework .permissions import AllowAny , IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserListAPIViews(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        users = ShopUser.objects.all()
        serializer = ShopUserSerializer(users, many=True)
        return Response(serializer.data)
