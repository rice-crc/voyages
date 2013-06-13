from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse

@override_settings(LANGUAGE_CODE='en')
class TestAuthentication(TestCase):
    """
    Test the basic login mechanism
    """
    def test_invalid_logininfo(self):
        """
        Attempt to login using an invalid username/password
        """
        # Should redirect
        response = self.client.post(reverse('contribute:index'), {'id_username': 'admin', 'id_password': 'should_not_work'})
        self.assertEqual(response.status_code, 302)
        
        # Should fail
        loginres = self.client.login(username='admin', password="random_pass")
        self.assertEqual(loginres, False)
  