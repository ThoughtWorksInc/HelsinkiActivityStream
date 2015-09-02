import http.server
import multiprocessing
import os

TEST_FIXTURE_SERVER_PORT = 3000


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
