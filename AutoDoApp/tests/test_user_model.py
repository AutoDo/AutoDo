from django.test import TestCase
from AutoDoApp.models import User


class UserModelTestCase(TestCase):

    def setUp(self):
        self.correct_email = "test@test.com"
        self.wrong_email = "abcd.com"
        self.wrong_length_email = "@"
        self.correct_account_ID = "test_account"
        self.wrong_account_ID = " "

    def test_wrong_email_should_raise_value_error(self):
        self.assertRaises(ValueError, User, self.wrong_email, self.correct_account_ID)

    def test_wrong_length_email_should_raise_value_error(self):
        self.assertRaises(ValueError, User, self.wrong_length_email, self.correct_account_ID)

    def test_correct_email_and_account_ID_should_not_raise_value_error(self):
        u = User(self.correct_email, self.correct_account_ID)
        self.assertIsNotNone(u)

    def test_wrong_account_ID_should_raise_value_error(self):
        self.assertRaises(ValueError, User, self.correct_email, self.wrong_account_ID)