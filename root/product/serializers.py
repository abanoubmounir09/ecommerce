
from rest_framework import serializers
<<<<<<< HEAD
from .models import Product,Category,Rating
=======
from .models import Product,Category,Order
>>>>>>> 18ca651dcd4ed33a7434a0feb0a1934e9107832a


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','PRDName','PRDCategory','PRDDesc','PRDImage','PRDPrice','PRDDiscountPrice','PRDCost','no_of_rating','avg_of_rating']


class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['CATName']


<<<<<<< HEAD
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields=['id','RATProduct','RATUser','stars']
=======

class orderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['Orderproduct']
>>>>>>> 18ca651dcd4ed33a7434a0feb0a1934e9107832a
