from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }
        # The password field is write-only to ensure it is not returned in API responses

    def create(self, validated_data):
        return User.objects.create_user(**validated_data) # Use create_user to handle password hashing, User.objects.create(...)
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)