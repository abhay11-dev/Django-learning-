from django.test import TestCase
from django.contrib.auth.models import User

class UserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser")

    def test_user_created(self):
        self.assertEqual(self.user.username, "testuser")