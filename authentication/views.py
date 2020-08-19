import jwt
from django.conf import settings
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView
from authentication.serializers import RegistrationSerializer, LoginSerializer, PasswordResetSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from authentication.models import User
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, password_validation
from django.contrib.sites.shortcuts import get_current_site


class RegistrationAPIView(GenericAPIView):
    """Register new users."""
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        response = {
            "data": {
                "user": user_data,
                "message": "user created successfully"
            }
        }

        # response not user_data --> develop
        # we user user_data because of open api
        return Response(user_data, status=status.HTTP_201_CREATED)


class FetchUsersAPIView(ListAPIView):
    """Register new users."""
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return User.objects.all().filter(role='AG')


class LoginAPIView(GenericAPIView):
    """ api view for logging in """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data
        repsonse = {
            "data": {
                "user": dict(user),
                "message": "You have successfuly logged in"
            }
        }
        return Response(repsonse, status=status.HTTP_200_OK)


class UserListDetailView(RetrieveAPIView):
    """ fetch a single user """
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return User.objects.all()

    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class PasswordUpdateAPIView(UpdateAPIView):
    """Endpoint for changing password for already logged in users"""

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    # The URL conf should include a keyword argument corresponding to this field
    lookup_url_kwarg = 'token'

    def update(self, request, *args, **kwargs):
        token = self.kwargs.get(self.lookup_url_kwarg)
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({"Message": "New password is required."}, status=status.HTTP_404_NOT_FOUND)

        try:
            decoded_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256']
            )
            user = user.objects.get(email=decoded_token['email'])
            user.set_password(new_password)
            user.save()

            return Response({"Message": "Password updated successfully."}, status=status.HTTP_201_CREATED)

        except:
            return Response({"Message": "Password could not be reset!"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(CreateAPIView):
    """Endpoint for reseting password for not logged in users"""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data['email']

        if not data:
            return Response(
                {"Message": "Provide your email for password reset"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if email exists in the system
        if not get_user_model().objects.filter(email=data).exists():
            raise ValidationError('Invalid email address')

        try:
            user = User.objects.get(email=data)
            token = PasswordResetAPIView.generate_password_reset_token(data)

            serializer = self.serializer_class(user)
            subject = "Password Reset"
            body = "Click this link to reset your password " + \
                f"https://{get_current_site(request)}/api/users/update_password/{token}"
            recipient = [serializer['email'].value, ]
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, body, sender, recipient, fail_silently=True)

            return Response(
                {"Message": "Check your email for a password reset link", "token": token},
                status=status.HTTP_201_CREATED
            )

        except:
            return Response(
                {"Message": "User not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def generate_password_reset_token(data):
        token = jwt.encode({
            'email': data
        }, settings.SECRET_KEY, algorithm="HS256")

        return token.decode('utf-8')
