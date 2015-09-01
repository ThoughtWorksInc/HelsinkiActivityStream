import unittest
import flask.json

import main


class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.app = main.app.test_client()


class BootstrapTest(MainTestCase):

    def test_root_serves_json(self):
        response = self.app.get('/')
        response_as_dictionary = flask.json.JSONDecoder().decode(response.get_data().decode())
        assert response_as_dictionary['a'] == 1
        assert response_as_dictionary['b'] == 'This  is a test!'

if __name__ == '__main__':
    unittest.main()
