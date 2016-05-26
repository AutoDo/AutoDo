from django.test import TestCase


# Create your tests here.
class BasicTestCase(TestCase):
    def setUp(self):
        pass

    def test_should_pass(self):
        self.assertEqual(True, True)
