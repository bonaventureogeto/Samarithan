from authentication.views import (RegistrationAPIView,
                                  LoginAPIView,
                                  FetchUsersAPIView,
                                  UserListDetailView,
                                  PasswordUpdateAPIView,
                                  PasswordResetAPIView)
from django.urls import path


urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('users', FetchUsersAPIView.as_view(), name='fetch_users'),
    path('users/<int:id>', UserListDetailView.as_view(), name='get-user'),
    path('reset_password/', PasswordResetAPIView.as_view(), name='reset-password'),
    path('update_password/<token>',
         PasswordUpdateAPIView.as_view(), name='update-password')
]
