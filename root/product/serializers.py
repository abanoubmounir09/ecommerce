
from rest_framework import serializers
from .models import Product,Category,Rating


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