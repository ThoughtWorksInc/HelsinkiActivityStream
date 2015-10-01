import unittest
import openahjo_activity_streams.scrape_and_push as sap


def scraper_returning(results):
    def scrape():
        return results

    return scrape


def add_one(item):
    return item + 1


class Pusher:
    def __init__(self):
        self._pushed_items = []

    def push(self, item):
        self._pushed_items.append(item)

    def pushed_items(self):
        return self._pushed_items


class ScrapeAndPushTest(unittest.TestCase):
    def test__it_gets_most_recent_timestamp_from_push_endpoint(self):
        pusher = Pusher()
        event = sap.scrape_and_push(scrape=scraper_returning([1, 2, 3]), convert=add_one, push=pusher.push)

        event()

        self.assertEquals(pusher.pushed_items(), [2, 3, 4])
