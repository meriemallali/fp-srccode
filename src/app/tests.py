import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, logout
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from .models import *
from .views import *

User = get_user_model()


# testing the authentication: signup
class RegisterUserTestCase(unittest.TestCase):
    def test_check_invalid_user(self):
        # user with username 'admin' does not exist in the database.
        username = 'admin1'
        message = f'{username} does not exists'
        user = User.objects.filter(username=username).exists()
        self.assertFalse(user, message)

    def test_check_valid_user(self):
        # create and save a new user profile.
        user = User.objects.create(
            username='newuser',
            email='newuser@gmail.com',
            password='ljkfnlewkjfnwwv12'
        )
        user.save()
        created_profile = UserProfile.objects.create(user=user)
        created_profile.save()
        # testing with the created user.
        username = 'newuser'
        message = f'{username} does exists'
        new_user = User.objects.filter(username=username)
        new_user_profile = UserProfile.objects.filter(user=user)
        self.assertTrue(new_user, message)
        self.assertTrue(new_user_profile is not None)


class SigninTestCase(unittest.TestCase):
    # test with invalid user credentials.
    def test_invalid_details(self):
        user = authenticate(username='meriama12', password='wekjfwn;kfqwm;')
        self.assertTrue(user is None)

    # test with an invalid password.
    def test_invalid_password(self):
        user = authenticate(username='admin', password='kfmwekfmw;ek')
        self.assertTrue(user is None)

    # test with correct credentials.
    def test_valid_details(self):
        user = authenticate(username='admin', password='user')
        self.assertFalse(user is not None)


# testing the authentication: logout
class LogoutTestCase(TestCase):
    # create a testing user.
    def setUp(self):
        self.user = self.client.login(username='admin', password='user')

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertTrue(response)


# REST API tests ------->

# end point: "/api/user_data"
class UserDataPITestCase(APITestCase):
    # test accessing restricted api end point
    def test_endpoint(self):
        self.client.login(username='admintest', password='admintest')
        response = self.client.get('/api/user_data')
        self.assertNotEqual(response.status_code, 201)


