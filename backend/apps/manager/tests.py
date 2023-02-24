import os
from unittest.mock import patch

from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User


class UserTest(APITestCase):
    def setUp(self):
        default_user = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        self.test_user = User.objects.create_user(**default_user)
        self.reset_url = reverse("user-password-reset")

    def test_password_reset_email(self):
        data = {
            "email": "test@example.com",
        }
        mail_message = "Follow this link to activate your account."

        with patch("apps.users.views.render_to_string", return_value=mail_message) as render:
            response = self.client.post(self.reset_url, data, format="json")

        data_user = User.objects.get(email=data.get("email"))
        render.assert_called_once()
        self.assertEqual(mail.outbox[0].subject, "Password reset")
        self.assertEqual(
            mail.outbox[0].body,
            mail_message,
        )
        self.assertEqual(mail.outbox[0].from_email, os.environ["DEFAULT_FROM_EMAIL"])
        self.assertEqual(mail.outbox[0].to, [data_user.email])
        self.assertTrue(User.objects.get(email=data.get("email")) in User.objects.all())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
