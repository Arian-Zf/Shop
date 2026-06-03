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
from orders.models import Order
from .permissions import IsAdminTabriz, IsBuyer

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
        min_discount = request.query_params.get('min_discount', 0)
        try:
            min_discount = int(min_discount)
        except ValueError:
            return Response({'error': 'Invalid value for min_discount'}, status=400)
        products = self.queryset.filter(off__gt=min_discount)
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


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminTabriz]


    
class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsBuyer]