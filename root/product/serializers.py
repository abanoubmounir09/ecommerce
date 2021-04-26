
from rest_framework import serializers
from .models import Product,Category,Rating
from .models import Product,Category,Order,OwnerProduct


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','PRDName','PRDCategory','PRDDesc','PRDQuantity','PRDImage','PRDPrice','PRDDiscountPrice','PRDCost','no_of_rating','avg_of_rating']


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


class ownerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=OwnerProduct
        fields='__all__'

"""
class prdownerSerializer(serializers.ModelSerializer):
    prd = productSerializer(read_only=True)
    prd_id = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='prd', write_only=True)

    class Meta:
        model = Product
        fields = ['prd', 'prd_id']
"""

"""
class prdownerSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = ['tracks']

"""












