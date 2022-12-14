"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase

class ViewTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(ViewTest, cls).setUpClass()
            django.setup()

    """ Tests that pages load correctly """
    def test_home(self):
        """Tests the home page."""
        response = self.client.get('/', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_contact(self):
        """Tests the contact page."""
        response = self.client.get('/contact/', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_about(self):
        """Tests the about page."""
        response = self.client.get('/about', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_game(self):
        """Tests the game page."""
        response = self.client.get('/game', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_login(self):
        """Tests the login page."""
        response = self.client.get('/login', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_map(self):
        """Tests the map page."""
        response = self.client.get('/map', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_profile(self):
        """Tests profile page."""
        response = self.client.get('/profile', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_show_user_profile(self):
        """Tests show user profile page."""
        response = self.client.get('/show_user_profile/', follow=True)
        self.assertEquals(response.status_code, 404)
        response = self.client.get('/show_user_profile/TlMytGMsweQG5aPeD5FuypLyIVv2/', follow=True) 
        self.assertEquals(response.status_code, 200)

    def test_whatwedo(self):
        """Tests what we do page."""
        response = self.client.get('/whatwedo', follow=True)
        self.assertEquals(response.status_code, 200)