# users/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile # <-- Import the Profile model

# 1. User Registration Serializer (Existing)
class UserSerializer(serializers.ModelSerializer):
    # ... (Keep the existing code for registration)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# 2. Profile Serializer (NEW)
class ProfileSerializer(serializers.ModelSerializer):
    # Read-only fields from the linked User model
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        # 'user' is the one-to-one foreign key, but we access its fields via source='user.field'
        fields = ('username', 'email', 'bio', 'profile_picture')
        read_only_fields = ('username', 'email') # These are managed by the User model, not here