# Copyright (c) 2015 ThoughtWorks
#
# See the file LICENSE for copying permission.

import http.server
import multiprocessing
import os
import unittest

TEST_FIXTURE_SERVER_PORT = 5000


class TestFixtureRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super(TestFixtureRequestHandler, self) \
            .__init__(request, client_address, server)
        self.extensions_map.update({'.json': 'application/json'})


def start_server():
    test_fixture_server = http.server.HTTPServer(
        ('', TEST_FIXTURE_SERVER_PORT),
        TestFixtureRequestHandler
    )
    os.chdir("./tests/resources")
    test_fixture_server.serve_forever()


class TestServer(object):
    def __init__(self):
        self._process = multiprocessing.Process(target=start_server)
        self._process.start()

    def stop(self):
        self._process.terminate()


class WithTestServer(unittest.TestCase):
    def setUp(self):
        self._test_data_server = TestServer()

    def tearDown(self):
        self._test_data_server.stop()
