import unittest
from app import app

class TestVoiceTranslationApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_record_endpoint(self):
        # Test the /record endpoint with a sample input
        response = self.app.post('/record')
        data = response.get_json()

        # Check if the response contains the expected keys
        self.assertIn('message', data)
        self.assertIn('status', data)

        # Adjust assertions based on the actual response structure
        if 'error' in data['status']:
            # This handles the case where an error occurred
            self.assertTrue(data['message'])  # Check that the error message is not empty
        else:
            # This handles the case where the request was successful
            self.assertIn('detected_text', data)
            self.assertIn('to_lang', data)
            self.assertIn('translated_text', data)
            self.assertIn('audio_file', data)

if __name__ == '__main__':
    unittest.main()
