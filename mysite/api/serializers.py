from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile
import re

User = get_user_model()
EGY_PHONE_REGEX = r'^(01[0125]\d{8})$'  

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)
    phone = serializers.CharField()

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_phone(self, value):
        if not re.match(EGY_PHONE_REGEX, value):
            raise serializers.ValidationError("Invalid Egyptian phone number.")
        if Profile.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        phone = validated_data['phone']

        
        base_username = email.split('@')[0] or 'user'
        username = base_username
        counter = 0
        while User.objects.filter(username=username).exists() or username == '':
            counter += 1
            username = f"{base_username}_{counter}"

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=False
        )
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(user=user, phone=phone)

        return {"user": user, "activation_code": profile.activation_code}
