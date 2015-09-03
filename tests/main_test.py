# Copyright (c) 2015 ThoughtWorks
#
# See the file LICENSE for copying permission.

import unittest

import flask.json
from openahjo_activity_streams import convert, main
import tests.data_server
import json


class WithTestServer(unittest.TestCase):
    def setUp(self):
        self._test_data_server = tests.data_server.TestServer()

    def tearDown(self):
        self._test_data_server.stop()


class BootstrapTest(WithTestServer):
    def setUp(self):
        super(BootstrapTest, self).setUp()
        self.app = main.create_app(
            remote_url='http://localhost:3000/test.json',
            converter=convert.identity_converter).test_client()

    def test_root_serves_json(self):
        response_data = self.app.get('/').get_data().decode()
        response_as_dictionary = flask.json.JSONDecoder() \
            .decode(response_data)
        assert response_as_dictionary['a'] == 1
        assert response_as_dictionary['b'] == 'This is a test!'


def load_json_from_file(file_name):
    path = './tests/resources/{:s}'.format(file_name)
    with open(path, 'r') as f:
        return json.load(f)


class EndToEndTest(WithTestServer):
    def setUp(self):
        super(EndToEndTest, self).setUp()
        self.app = main.create_app(
            remote_url='http://localhost:3000/openahjo-small-data.json',
            converter=convert.to_activity_stream).test_client()

    def test_end_to_end_with_stub_data(self):
        response_data = self.app.get('/').get_data().decode()
        response_as_dictionary = json.loads(response_data)
        expected_data = load_json_from_file('activity-stream-small-data.json')
        self.assertEquals(response_as_dictionary, expected_data)


if __name__ == '__main__':
    unittest.main()
