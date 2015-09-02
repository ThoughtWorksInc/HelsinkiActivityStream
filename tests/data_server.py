import http.server
import multiprocessing
import os


TEST_FIXTURE_SERVER_PORT = 3000


class TestFixtureRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super(TestFixtureRequestHandler, self).__init__(request, client_address, server)
        self.extensions_map.update(
            {'.json': 'application/json'}
        )


class TestServer(object):
    def __init__(self):
        self._process = multiprocessing.Process(target=self.set_server)
        self._process.start()

    def set_server(self):
        self._test_fixture_server = http.server.HTTPServer(
            ('', TEST_FIXTURE_SERVER_PORT),
            TestFixtureRequestHandler
        )
        os.chdir("./tests/resources")
        self._test_fixture_server.serve_forever()

    def inner_stop(self):
        self._test_fixture_server.server_close()

    def stop(self):
        self._process.terminate()