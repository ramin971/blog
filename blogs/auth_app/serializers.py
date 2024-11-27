from rest_framework_simplejwt.serializers import TokenRefreshSerializer as BaseTokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password 
# from django.db import transaction
from .models import User


class TokenRefreshSerializer(BaseTokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        # print('****',self.context['request'].COOKIES)
        if attrs['refresh']:
            return super().validate(attrs)
        raise InvalidToken
    

class UserCreateSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id','username','password','access']
        extra_kwargs = {'id':{'read_only':True},'password':{'write_only':True}}

    def validate_password(self,value):
        validate_password(value)
        return value

    # # validate just user data to prevent error
    # def validate(self, attrs):
    #     customer=attrs.pop('customer')
    #     super().validate(attrs)
    #     attrs['customer'] = customer
    #     return attrs
    
    # take access token to new user response
    def get_access(self,instance):
        refresh_token = RefreshToken.for_user(instance)
        access_token = refresh_token.access_token
        return str(access_token)
    
    # create customer beside user
    # @transaction.atomic()
    # def create(self, validated_data):
    #     customer_data = validated_data.pop('customer')
    #     user = super().create(validated_data)
    #     customer = Customer.objects.create(user=user,**customer_data)
    #     return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password']
        # extra_kwargs = {'id':{'read_only':True},'password':{'write_only':True}}


    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']
        read_only_fields = ['id']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True , write_only=True)
    new_password = serializers.CharField(required=True , write_only=True)

    def validate_old_password(self,value):
        user = self.context['user']
        print('3333333333333',user)
        if not user.check_password(value):
            raise serializers.ValidationError('Your old password was entered incorrectly.')
        return value
    
    def validate_new_password(self,value):
        validate_password(value)
        return value
    
    def save(self, **kwargs):
        user = self.context['user']
        password = self.validated_data['new_password']
        user.set_password(password)
        user.save()
        return user