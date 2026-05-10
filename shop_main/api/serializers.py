from rest_framework import serializers
from account.models import ShopUser
from shop.models import *


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ('name', 'value')


class ProductSerializer(serializers.ModelSerializer):
    features = ProductFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'new_price', 'features']


#new
class ShopUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ('id', 'phone', 'first_name', 'last_name', 'address', 'is_staff', 'date_joined', 'is_active')
