from rest_framework.fields import empty
from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError

#create the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username", "email", "first_name", "last_name", "date_joined", "is_customer", "is_staff", "is_active"]

#serializer to enable user login
class obtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        token['is_customer'] = user.is_customer
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email 

        return token
    
#serializer to enable user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    confirm_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'last_name', 'first_name', 'password', 'confirm_password', 'is_staff','is_customer']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        try:
            user = User.objects.create(
                username=validated_data['email'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                is_staff=validated_data.get('is_staff', False),
                is_customer=validated_data.get('is_customer', False),
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
        except IntegrityError:
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        
#serializer to manage books
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

#serializers to manage reservations
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ['id', 'copies','contact','reservation_date','status', 'user', 'book']

    def to_representation(self, instance):
        response =  super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['book'] = BookSerializer(instance.book).data
        return response
    
#user resevertions
class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ['id', 'copies','contact','reservation_date','status', 'book']

    def to_representation(self, instance):
        response =  super().to_representation(instance)
        response['book'] = BookSerializer(instance.book).data
        return response

class UserReservationSerializer(serializers.ModelSerializer):
    reserve = ReservationsSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ['id', 'reserve']