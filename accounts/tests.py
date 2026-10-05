from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AccountTests(TestCase):
    def test_registration_and_login(self):
        response = self.client.post(reverse('accounts:register'), {'username':'newuser','email':'new@example.com','first_name':'New','last_name':'User','password1':'A-strong-pass123','password2':'A-strong-pass123'})
        self.assertRedirects(response, reverse('blog:dashboard'))
        self.client.post(reverse('accounts:logout'))
        response = self.client.post(reverse('accounts:login'), {'username':'newuser','password':'A-strong-pass123'})
        self.assertEqual(response.status_code, 302)
