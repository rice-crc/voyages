from django.test import TestCase
class UserOrEmailTest(TestCase):

    fixtures = ['users.json']

    def test_login(self):
        # using username with bad password
        result = self.client.login(username='testuser', password='xxxxxx')
        self.assertFalse(result)

        # using username with good password
        result = self.client.login(username='testuser', password='testuser')
        self.assertTrue(result)

        # using email with bad password
        result = self.client.login(username='test@user.com', password='xxxxxx')
        self.assertFalse(result)

        # using email with good password
        result = self.client.login(username='test@user.com', password='testuser')
        self.assertTrue(result)