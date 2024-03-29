from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    registered_at = serializers.DateTimeField(format="%H:%M %d.%m.%Y", read_only=True)

    avatar = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    short_name = serializers.SerializerMethodField(read_only=True)

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else settings.STATIC_URL + "images/default_avatar.png"

    def get_full_name(self, obj):
        return obj.full_name + "sadasd"

    def get_short_name(self, obj):
        return obj.short_name

    class Meta:
        model = User
        fields = ["email", "avatar", "full_name", "short_name", "registered_at", "id", "is_admin"]


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]


class TokenAccessObtainSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "Invalid username or password",
    }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user.is_staff:
            token["role"] = "stuff"
        if user.is_superuser or user.is_admin:
            token["role"] = "admin"

        return token
