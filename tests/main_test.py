import unittest

import flask.json
from openahjo_activity_streams import convert, main
import tests.data_server
import json


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = main.get_test_client()


class BootstrapTest(MainTestCase):
    def setUp(self):
        main \
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


def load_json_from_file(file_name):
    path = './tests/resources/{:s}'.format(file_name)
    with open(path, 'r') as f:
        return json.load(f)


@unittest.skip("20150902 DM + RP --- ignored until converter implemented")
class EndToEndTest(MainTestCase):
    def setUp(self):
        main.set_remote_url('http://localhost:3000/openahjo-small-data.json')
        super(EndToEndTest, self).setUp()
        self._test_data_server = tests.data_server.TestServer()

    def tearDown(self):
        self._test_data_server.stop()
        super(EndToEndTest, self).tearDown()

    def test_end_to_end_with_stub_data(self):
        main.set_converter_to(convert.to_activity_stream)
        response_data = self.app.get('/').get_data().decode()
        response_as_dictionary = json.loads(response_data)
        expected_data = load_json_from_file('activity-stream-small-data.json')
        self.assertEquals(response_as_dictionary, expected_data)


if __name__ == '__main__':
    unittest.main()
