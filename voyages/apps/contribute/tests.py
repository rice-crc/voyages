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

    fixtures = ['users.json']

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

    def test_invalid_login_info(self):
        """
        Attempt to login using an invalid username/password
        """
        # Should redirect
        response = self.client.post(reverse('contribute:index'),
                                    {'id_username': 'admin', 'id_password': 'should_not_work'}, follow=True)
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/contribute/login/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('contribute:login'),
                                    {'id_username': 'admin', 'id_password': 'should_not_work'})
        self.assertEqual(response.status_code, 200)
        # Should display the error message
        self.assertContains(response, "Your username/email and password didn't match. Please try again")

        # Should fail
        login_res = self.client.login(username='admin', password="random_pass")
        self.assertEqual(login_res, False)

        # Should redirect, since we are not logged in
        response = self.client.get(reverse('contribute:index'), follow=True)
        self.assertRedirects(response, reverse('contribute:login'), status_code=302, target_status_code=200)


    def test_valid_login_info(self):
        """
        Attempt to login using a valid combination of user name and password
        """
        # Create a user
        user_obj, usr_name, usr_password = self.create_random_user()

        # Perform login then check if we can access the user_index page
        login_res = self.client.login(username=usr_name, password=usr_password)
        self.assertEqual(login_res, True)
        response = self.client.get(reverse('contribute:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to the Contribute Section")
        # Not a staff user
        self.assertNotContains(response, "Live Admin")

        user_obj.is_staff=True
        user_obj.save()
        login_res = self.client.login(username=usr_name, password=usr_password)
        self.assertEqual(login_res, True)
        response = self.client.get(reverse('contribute:index'))
        self.assertEqual(response.status_code, 200)

        #Is a staff user
        self.assertContains(response, "Live Admin")


    def test_user_or_email(self):
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