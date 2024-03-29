from django.contrib.auth import get_user_model

from rest_framework import serializers
from authentication.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, password_validation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'un_id']


class RegistrationSerializer(serializers.ModelSerializer):
    """Serialize registration requests and create a new user."""

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.ChoiceField(choices=[('PA', 'POLITICIAN ADMIN'), ('AG', 'AGENT'), ('CM', 'CAMPAIGN MANAGER')])

    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            "min_length": "Password should be at least {min_length} characters"
        }
    )
    confirmed_password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            "min_length": "Password should be at least {min_length} characters"
        }
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "un_id",
                  "password", "confirmed_password", "role"]

    def validate(self, data):
        """Validate data before it gets saved."""

        confirmed_password = data.get("confirmed_password")
        try:
            validate_password(data["password"])
        except ValidationError as identifier:
            raise serializers.ValidationError({
                "password": str(identifier).replace(
                    "["", "").replace(""]", "")})

        if not self.do_passwords_match(data["password"], confirmed_password):
            raise serializers.ValidationError({
                "passwords": ("Passwords do not match")
            })

        return data

    def create(self, validated_data):
        """Create a user."""
        del validated_data["confirmed_password"]
        return User.objects.create_user(**validated_data)

    def do_passwords_match(self, password1, password2):
        """Check if passwords match."""
        return password1 == password2


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, style={'placeholder': 'Email', 'autofocus': True})
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True, style={'input_type': 'password', 'placeholder': 'Password'})
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError({
                "invalid": "invalid email and password combination"
            })

        user = {
            "email": user.email,
            "token": user.token
        }
        return user


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password change endpoint"""

    new_password = serializers.CharField(
        max_length=50, label=("new password"), style={'input_type': 'password'}, required=True)
