from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
import random
from django.contrib.auth.models import User

@override_settings(LANGUAGE_CODE='en')
class TestAuthentication(TestCase):
    """
    Test the basic login mechanism of the Admin site
    """
    def create_random_user(self):
        """
        Create a user with the specified username and password
        Return the object, username and password
        """
        username = "test_user" + str(random.randint(0, 1000000))
        password = "test_user" + str(random.randint(0, 100000))
        
        tmpUser = User.objects.create(username=username)
        tmpUser.set_password(password)
        tmpUser.save()
        return tmpUser, username, password
    
    def test_invalid_logininfo(self):
        """
        Attempt to login using an invalid username/password
        """
        # Should redirect
        response = self.client.post(reverse('contribute:index'), {'id_username': 'admin', 'id_password': 'should_not_work'})
        self.assertEqual(response.status_code, 302)
        
        response = self.client.post(reverse('contribute:login'), {'id_username': 'admin', 'id_password': 'should_not_work'})
        self.assertEqual(response.status_code, 200)
        
        # Should fail
        loginres = self.client.login(username='admin', password="random_pass")
        self.assertEqual(loginres, False)
        
        # Should redirect, since we are not logged in
        response = self.client.get(reverse('contribute:user_index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Welcome to the Contribute Section")
  
    def test_valid_logininfo(self):
        """
        Attempt to login using a valid combination of user name and password
        """
        # Create a user
        user_obj, usr_name, usr_passwd = self.create_random_user()
        
        # Perform login then check if we can access the user_index page
        loginres = self.client.login(username=usr_name, password=usr_passwd)
        self.assertEqual(loginres, True)
        response = self.client.get(reverse('contribute:user_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to the Contribute Section")
