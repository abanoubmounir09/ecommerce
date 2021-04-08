
from rest_framework import serializers
from .models import Product,Category


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['PRDName','PRDCategory','PRDDesc','PRDImage','PRDPrice','PRDDiscountPrice','PRDCost']


class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['CATName']