from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course
from .models import UserProgress
from .models import Purchase

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'price')

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ('id', 'user', 'course', 'completed')

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('id', 'user', 'course', 'date_purchased')
        read_only_fields = ('user', 'date_purchased')

class ProfileSerializer(serializers.ModelSerializer):
    purchases = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'purchases')
