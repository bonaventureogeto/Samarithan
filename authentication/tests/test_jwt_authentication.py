from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import exceptions

from authentication.tests.factories.authentication_factory import UserFactory
from authentication.backends import JWTAuthentication
from authentication.models import User

import jwt


class JWTAuthenticationTest(TestCase):
    """ Test jwt authentication """

    def setUp(self):
        self.user = UserFactory.create(
            first_name='kelvin', last_name='onkundi')
        self.user_token = self.user.token
        self.user.save()
        self.jwt_auth = JWTAuthentication()
        self.client = APIClient()
        self.factory = APIRequestFactory()

        self.token_expiry = datetime.now() - timedelta(hours=40)

        self.expired_token = jwt.encode({
            'id': self.user.pk,
            'email': self.user.email,
            'exp': int(self.token_expiry.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

    def test_authentication_failure_because_header_is_none(self):
        """ 
        test if authentication if the request fails with authorization 
        header of zero
        """
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = ''
        res = self.jwt_auth.authenticate(request)
        self.assertEqual(res, None)

    def test_authentication_if_length_is_one(self):
        """ test if the length of the token is one """
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearersjsalkjjlkjdlakjdlsjd'
        res = self.jwt_auth.authenticate(request)
        self.assertEqual(res, None)

    def test_authentication_if_length_is_greater_than_2(self):
        """ test authentication if length is greater than two """
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = "Kelvin Kelvin Kelvin"
        res = self.jwt_auth.authenticate(request)
        self.assertEqual(res, None)

    def test_authentication_prefix_is_not_bearer(self):
        """ test the prefix is not Bearer"""
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = "Beaewrer tokenfskfjsldfslfj"
        res = self.jwt_auth.authenticate(request)
        self.assertEqual(res, None)

    def test_authenticate_user_correctly(self):
        """" test token auth works """
        request = self.factory.get("/")
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.user_token}'
        res = self.jwt_auth.authenticate(request)
        self.assertEqual(res[0].email, self.user.email)

    def authenticate_failed_with_expired_token(self):
        """ test auth with expired token fails """
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer, {}'.format(
            self.expired_token)
        with self.assertRaises(exceptions.AuthenticationFailed) as e:
            res = self.jwt_auth._authenticate_credentials(
                request, self.expired_token
            )
        self.assertEqual(str(e.exception),
                         'Your token has expired, please login again.')

    def test_token_validated(self):
        """" test token auth works """
        request = self.factory.get("/")
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.user_token}'
        res = self.jwt_auth._authenticate_credentials(request, self.user_token)
        self.assertEqual(res[0].email, self.user.email)

    def test_authentication_failure_incase_of_decoding_error(self):
        """We unit test our authentication method to see if the method
        returns decoding error when supplied with invalid"""
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer, {}'.format('fake-token')
        with self.assertRaises(exceptions.AuthenticationFailed) as e:
            res = self.jwt_auth._authenticate_credentials(
                request, 'fake-token')
        self.assertEqual(str(e.exception), 'Not enough segments')

    def test_authentication_failure_if_user_non_existent(self):
        """We unit test our authentication method to see if the method
        returns error message when supplied with a non existent user"""
        non_existing = User.objects.create_user(
            first_name='trial', last_name='trial2', email='trial@trial.com', password='triall')
        non_existing.delete()
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer, {}'.format(
            non_existing.token)
        with self.assertRaises(exceptions.AuthenticationFailed) as e:
            res = self.jwt_auth._authenticate_credentials(
                request, non_existing.token)
        self.assertEqual(
            str(e.exception), 'User matching this token was not found.'
        )

    def test_authentication_failure_if_user_not_active(self):
        """We unit test our authentication method to see if the method
        returns error message when supplied with an inactive user"""
        non_existing = User.objects.create_user(
            first_name='trial', last_name='trial2', email='trial@trial.com', password='triall')
        non_existing.is_active = False
        non_existing.save()
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer, {}'.format(
            non_existing.token)
        with self.assertRaises(exceptions.AuthenticationFailed) as e:
            res = self.jwt_auth._authenticate_credentials(
                request, non_existing.token)
        self.assertEqual(
            str(e.exception), 'Forbidden! This user has been deactivated.'
        )
