# from rest_framework import serializers
from django.contrib.auth.models import User



from rest_framework import serializers
from django.contrib.auth.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','is_staff')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','is_staff')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user



class userSerializer(serializers.ModelSerializer):
    # password2= serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','username','password']#,'password2'
        # extra_kwargs={
        #     'password':{'write_only':True}
        # }

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user

    def save(self):
        userOb=User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            
        )
        password=self.validated_data['password']
        # password2=self.validated_data['password2']

        # if password != password2:
        #     raise serializers.ValidationError({'password':' password not match'})
        userOb.set_password(password)
        userOb.save()
        return userOb
        