from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'email','is_staff','token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)