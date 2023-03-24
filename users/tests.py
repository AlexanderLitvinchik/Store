from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from users.models import User, EmailVerification
from users.forms import UserRegistrationForm

from datetime import timedelta
from django.utils.timezone import now


# Create your tests here.

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'Александр',
            'last_name': 'Литвинчик',
            'username': 'admin2',
            'email': 'adin@mail.ru',
            'password1': '1',
            'password2': '2'
        }
        # проверка get запроса

    def test_user_registration_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertEqual(response.context_data['title'], 'Store - Регистрация ')
        # проверка что используется нужный шаблон
        self.assertTemplateUsed(response, 'users/registration.html')

    # проверка пост запроа

    def test_user_registration_post_success(self):
        username = self.data['username']
        # gпроверяем что пользователь не был моздан в системе
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.data)

        # какая-то мистика почему status_code выдает 200
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # проверка куда перенапрявится пользователь
        self.assertRedirects(response, reverse('users:login'))
        # проверяем если такой пользователь
        self.assertTrue(User.objects.filter(username=username).exists())

        # cretinhg of email verification
        email_verification = EmailVerification.objects.filter(user_username=username)
        self.assertTrue(email_verification.exists())
        # cheking date
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() * timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        # проверка того что нельзя содать пользователя с таким же username
        username = self.data['username']
        user = User.objects.create(username=username)
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
