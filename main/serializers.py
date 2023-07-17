from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import serializers
from captcha.fields import ReCaptchaField



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class NewPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class ProfileSerializer(UserSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ReCaptchaSerializerField(serializers.Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recaptcha = ReCaptchaField()

    def to_internal_value(self, data):
        return self.recaptcha.clean(data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    recaptcha = ReCaptchaSerializerField()


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        if user and user.is_active:
            attrs['user'] = user
            return attrs
        else:
            return serializers.ValidationError('Invalid credentials.')

class RegisterSerializer(serializers.ModelSerializer):
    recaptcha = ReCaptchaSerializerField()
    class Meta:
        model = User
        fields = ("id", "username", "password", "email")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        

class LikingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = '__all__'

