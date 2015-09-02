import unittest

import flask.json
import main
import tests.data_server


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = main.app.test_client()


class BootstrapTest(MainTestCase):
    def setUp(self):
        super(BootstrapTest, self).setUp()
        self._test_data_server = tests.data_server.TestServer()

    def tearDown(self):
        self._test_data_server.stop()
        super(BootstrapTest, self).tearDown()

    def test_root_serves_json(self):
        response = self.app.get('/')
        response_as_dictionary = flask.json.JSONDecoder().decode(response.get_data().decode())
        assert response_as_dictionary['a'] == 1
        assert response_as_dictionary['b'] == 'This is a test!'


if __name__ == '__main__':
    unittest.main()
