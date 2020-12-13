from rest_framework import serializers
from src.apis.authentication.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=64, min_length=6, write_only=True)

    enroll_no = serializers.CharField(
        max_length=15, min_length=15)

    class Meta:
        model = User
        fields = ['enroll_no', 'email', 'password']
   

    def validate(self, attrs):
        # enroll_no = attrs.get('enroll_no', '')
        email = attrs.get('email', '')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    enroll_no = serializers.CharField(max_length=15, min_length=15)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    email = serializers.EmailField(
        max_length=255, min_length=3, read_only=True)
    user_type = serializers.CharField(
        max_length=8, min_length=7, read_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['enroll_no', 'user_type', 'email', 'password', 'tokens']

    def validate(self, attrs):
        enroll_no = attrs.get('enroll_no', '')
        password = attrs.get('password', '')

        user = auth.authenticate(enroll_no=enroll_no, password=password)

        if not user:
            raise AuthenticationFailed(
                'Invalid Credentials!, Try again.')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled.')
        if not user.is_verified:
            raise AuthenticationFailed(
                'Please verify your email first.')

        return{
            'enroll_no': user.enroll_no,
            'email': user.email,
            'user_type': user.user_type,
            'tokens': user.tokens

        }
        return super().validate(attrs)
