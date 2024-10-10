from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Project, Task
from datetime import date
from .serializers import ProjectSerializer, TaskSerializer


# Helper function to create a user
def create_user(username="testuser", password="testpassword"):
    return User.objects.create_user(username=username, password=password)

class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        """ Test creating a new user """
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com"
        }
        response = self.client.post(reverse('user_signup'), data)  # Make sure 'user_signup' exists in your urls.py
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)  # Ensure one user is created
        self.assertEqual(User.objects.get().username, "newuser")

    def test_user_registration_invalid(self):
        """ Test registration with invalid data (missing fields) """
        data = {
            "username": "",
            "password": ""
        }
        response = self.client.post(reverse('user_signup'), data)  # Ensure URL name consistency
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)  # Ensure no user is created
