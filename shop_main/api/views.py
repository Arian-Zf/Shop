from django.shortcuts import render
from shop.models import Product
from .serializers import *
from rest_framework import generics , viewsets
from rest_framework.views import APIView
from account.models import ShopUser
from rest_framework.response import Response
from rest_framework .permissions import AllowAny , IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action

# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class ProductDetailAPIView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['GET'], url_path="all_discount_products", url_name="all_discount_products",
            permission_classes=[IsAuthenticated])
    def discount_products(self, request):
        products = self.queryset.filter(off__gt=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
        

class UserListAPIViews(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        users = ShopUser.objects.all()
        serializer = ShopUserSerializer(users, many=True)
        return Response(serializer.data)

class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = ShopUser.objects.all()
    serializer_class = UserRegistrationSerializer