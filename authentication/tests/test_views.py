import json
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status


class UserTestViews(APITestCase):

    client = APIClient()

    def setUp(self):
        self.user = {

            "email": "kelvin.onkundi@andela.com",
            "password": "novak254",
            "first_name": "kelvin",
            "last_name": "onkundi",
            "confirmed_password": "novak254",
            "role": "GA"

        }

    def test_register_user(self):
        """ test for user registration """
        response = self.client.post(
            '/api/v1/auth/register/', self.user, format='json')
        result = json.loads(response.content)
        self.assertEqual(result['data']['user']['email'],
                         "kelvin.onkundi@andela.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        """
        test login
        """
        self.client.post(
            '/api/v1/auth/register/', self.user, format='json')

        # hit the API endpoint
        response = self.client.post(
            '/api/v1/auth/login/', self.user, format='json')
        result = json.loads(response.content)

        # self.assertIn(
        #     'Invalid email or password provided.', str(result))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
