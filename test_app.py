import unittest
from app import app

class TestGSUApp(unittest.TestCase):

    #This creates a Test Client (a fake browser) so we can talk to the app without actually having to open Chrome or start te server.
    def setUp(self):
        """This runs before every single test."""
        app.config['TESTING'] = True
        self.client = app.test_client() 

    def test_homepage_status(self):
        """Verify the login page returns a 200 OK status."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_protection(self):
        """Verify that unauthorized users are redirected (302)."""
        response = self.client.get('/dashboard', follow_redirects=False)
        self.assertEqual(response.status_code, 302) #302 is the status code for a redirect, which is what we expect if the user is not logged in.

    def test_app_name_in_html(self):
        """Verify the branding 'GSU' exists on the page."""
        response = self.client.get('/')
        self.assertIn(b"Georgia State", response.data)

if __name__ == '__main__':
    unittest.main()