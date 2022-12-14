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
        response = self.client.get('/')
        self.assertContains(response, 200)

    def test_contact(self):
        """Tests the contact page."""
        response = self.client.get('/contact')
        self.assertContains(response, 200)

    def test_about(self):
        """Tests the about page."""
        response = self.client.get('/about')
        self.assertContains(response, 200)

    def test_game(self):
        """Tests the game page."""
        response = self.client.get('/game')
        self.assertContains(response, 200)

    def test_login(self):
        """Tests the login page."""
        response = self.client.get('/login')
        self.assertContains(response, 200)

    def test_map(self):
        """Tests the map page."""
        response = self.client.get('/map')
        self.assertContains(response, 200)

    def test_profile(self):
        """Tests profile page."""
        response = self.client.get('/profile')
        self.assertContains(response, 200)

    def test_show_user_profile(self):
        """Tests show user profile page."""
        response = self.client.get('/show_user_profile/')
        self.assertContains(response, 404)
        response = self.client.get('/show_user_profile/TlMytGMsweQG5aPeD5FuypLyIVv2/') 
        self.assertContains(response, 200)

    def test_whatwedo(self):
        """Tests what we do page."""
        response = self.client.get('/whatwedo')
        self.assertContains(response, 200)

        
