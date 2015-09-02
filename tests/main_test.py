import unittest

import flask.json
import openahjo_activity_streams.main
import tests.data_server


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = openahjo_activity_streams.main.get_test_client()


class BootstrapTest(MainTestCase):
    def setUp(self):
        openahjo_activity_streams.main\
            .set_remote_url('http://localhost:3000/test.json')
        super(BootstrapTest, self).setUp()
        self._test_data_server = tests.data_server.TestServer()

    def tearDown(self):
        self._test_data_server.stop()
        super(BootstrapTest, self).tearDown()

    def test_root_serves_json(self):
        response_data = self.app.get('/').get_data().decode()
        response_as_dictionary = flask.json.JSONDecoder() \
            .decode(response_data)
        assert response_as_dictionary['a'] == 1
        assert response_as_dictionary['b'] == 'This is a test!'


if __name__ == '__main__':
    unittest.main()
