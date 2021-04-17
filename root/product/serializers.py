
from rest_framework import serializers
from .models import Product,Category,Rating
from .models import Product,Category,Order


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','PRDName','PRDCategory','PRDDesc','PRDImage','PRDPrice','PRDDiscountPrice','PRDCost','no_of_rating','avg_of_rating']


class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['CATName']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields=['id','RATProduct','RATUser','stars']

class orderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['Orderproduct']
