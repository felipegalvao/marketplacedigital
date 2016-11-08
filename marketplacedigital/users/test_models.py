from django.test import TestCase
from model_mommy import mommy

from django.contrib.auth.models import User
from .models import Profile

class UserTestMommy(TestCase):
    def test_user_creation_mommy(self):
        new_user = mommy.make(User)
        new_profile = Profile.objects.get(user=new_user)

        self.assertTrue(isinstance(new_user, User))
        self.assertTrue(isinstance(new_profile, Profile))

        self.assertEqual(new_user.__str__(), new_user.username)
        self.assertEqual(new_profile.__str__(), new_profile.user.username)
