
from rest_framework import serializers
from .models import Product,Category,Order


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','PRDName','PRDCategory','PRDDesc','PRDImage','PRDPrice','PRDDiscountPrice','PRDCost']


class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['CATName']



class orderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['Orderproduct']