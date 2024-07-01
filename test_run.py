import unittest
from unittest.mock import patch, MagicMock
import run
import requests

class TestRun(unittest.TestCase):

    @patch('run.os.getenv')
    def test_retrieve_input(self, mock_getenv):
        mock_getenv.return_value = 'test_value'
        self.assertEqual(run.retrieve_input('TEST_ENV'), 'test_value')
        mock_getenv.return_value = None
        with self.assertRaises(SystemExit):
            run.retrieve_input('TEST_ENV')

    def test_generate_authentication_headers(self):
        headers = run.generate_authentication_headers('test_token')
        expected_headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer test_token",
        }
        self.assertEqual(headers, expected_headers)

    @patch('run.requests.get')
    def test_retrieve_public_key_details(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'test_key'}
        mock_get.return_value = mock_response
        self.assertEqual(run.retrieve_public_key_details('http://test', 'token'), {'key': 'test_key'})

        mock_response.status_code = 404
        mock_get.return_value = mock_response
        mock_get.side_effect = requests.RequestException("Error")
        with self.assertRaises(SystemExit):
            run.retrieve_public_key_details('http://test', 'token')

    @patch('run.public.PublicKey')
    @patch('run.public.SealedBox')
    def test_encrypt_secret(self, mock_sealed_box, mock_public_key):
        mock_public_key.return_value = MagicMock()
        mock_sealed_box_instance = MagicMock()
        mock_sealed_box.return_value = mock_sealed_box_instance
        mock_sealed_box_instance.encrypt.return_value = b'encrypted_value'
        encrypted = run.encrypt_secret('test_key', 'utf-8', 'secret')
        self.assertEqual(encrypted, 'ZW5jcnlwdGVkX3ZhbHVl')

        mock_public_key.side_effect = Exception('Encryption error')
        with self.assertRaises(SystemExit):
            run.encrypt_secret('test_key', 'utf-8', 'secret')

    @patch('run.requests.put')
    def test_save_secret(self, mock_put):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_put.return_value = mock_response
        run.save_secret('http://test', 'token', 'key_id', 'secret_name', 'secret')

        mock_response.status_code = 400
        mock_put.return_value = mock_response
        mock_put.side_effect = requests.RequestException("Error")
        with self.assertRaises(SystemExit):
            run.save_secret('http://test', 'token', 'key_id', 'secret_name', 'secret')



if __name__ == '__main__':
    unittest.main()