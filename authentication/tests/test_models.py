from rest_framework.test import APITestCase, APIClient
from authentication.models import User
from authentication.serializers import RegistrationSerializer


class UserTest(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = {
            "email": "ndemo@gmail.com",
            "username": "novak",
            "password": "Lacazette@1998",
            "first_name": "kelvin",
            "last_name": "onkundi"
        }

    def test_create_superuser(self):
        """
        test create super user method
        """
        response = User.objects.create_superuser(
            self.user["first_name"], self.user["last_name"], self.user["email"], self.user["password"]
        )
        user = User.objects.filter(email="ndemo@gmail.com").first()
        self.assertEqual(user.email, 'ndemo@gmail.com')

    def test_create_superuser_no_password(self):
        """
        test user creation with no password
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_superuser(
                self.user['first_name'],
                self.user['last_name'],
                self.user['email']
            )
        self.assertEqual(str(error_message.exception),
                         'Superusers must have a password.')

    def test_create_superuser_no_email(self):
        """
        test user creation with no email
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_superuser(
                first_name=self.user['first_name'],
                last_name=self.user['last_name'],
                password=self.user['password']
            )
        self.assertEqual(str(error_message.exception),
                         'Superusers must have an email address.')

    def test_create_superuser_no_first_name(self):
        """
        test user creation with no first_name
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_superuser(
                password=self.user['password'],
                last_name=self.user['last_name'],
                email=self.user['email']
            )
        self.assertEqual(str(error_message.exception),
                         'Superusers must have a first name.')

    def test_create_superuser_no_last_name(self):
        """
        test user creation with no last name
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_superuser(
                password=self.user['password'],
                first_name=self.user['first_name'],
                email=self.user['email']
            )
        self.assertEqual(str(error_message.exception),
                         'Superusers must have a last name.')

    def test_super_user_role(self):
        """ test the default role for a super user"""
        response = User.objects.create_superuser(
            self.user["first_name"], self.user["last_name"], self.user["email"], self.user["password"]
        )
        user = User.objects.filter(email="ndemo@gmail.com").first()
        self.assertEqual(user.email, 'ndemo@gmail.com')
        self.assertEqual(user.role, 'GA')

    def test_create_user(self):
        """ create a user """
        response = User.objects.create_user(
            self.user["first_name"], self.user["last_name"], self.user["email"], self.user["password"]
        )
        user = User.objects.filter(email="ndemo@gmail.com").first()
        self.assertEqual(user.email, "ndemo@gmail.com")

    def test_create_user_no_first_name(self):
        """
        test user creation with no first_name
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_user(
                password=self.user['password'],
                last_name=self.user['last_name'],
                email=self.user['email']
            )
        self.assertEqual(str(error_message.exception),
                         'Users must have a first name.')

    def test_create_user_no_last_name(self):
        """
        test user creation with no last name
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_user(
                password=self.user['password'],
                first_name=self.user['first_name'],
                email=self.user['email']
            )
        self.assertEqual(str(error_message.exception),
                         'Users must have a last name.')

    def test_create_user_no_email(self):
        """
        test user creation with no email
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_user(
                first_name=self.user['first_name'],
                last_name=self.user['last_name'],
                password=self.user['password']
            )
        self.assertEqual(str(error_message.exception),
                         'Users must have an email address.')

    def test_create_user_no_password(self):
        """
        test user creation with no password
        """
        with self.assertRaises(TypeError) as error_message:
            User.objects.create_user(
                self.user['first_name'],
                self.user['last_name'],
                self.user['email']
            )
        self.assertEqual(str(error_message.exception),
                         'Users must have a password.')

    def test_user_representation(self):
        """ test user representation """
        response = User.objects.create_user(
            self.user["first_name"], self.user["last_name"], self.user["email"], self.user["password"]
        )
        user = User.objects.filter(email="ndemo@gmail.com").first()
        self.assertEqual(str(user), "ndemo@gmail.com")

    def test_get_email_property(self):
        """ test the get email property on user """
        response = User.objects.create_user(
            self.user["first_name"], self.user["last_name"], self.user["email"], self.user["password"]
        )
        user = User.objects.filter(email="ndemo@gmail.com").first()
        self.assertEqual(user.get_email, "ndemo@gmail.com")
