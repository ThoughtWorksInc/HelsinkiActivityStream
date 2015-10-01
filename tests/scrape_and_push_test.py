import unittest
import openahjo_activity_streams.exceptions as ex
import openahjo_activity_streams.scrape_and_push as sap


def scraper_returning(results):
    def scrape():
        return results

    return scrape


def failing_scraper():
    raise ex.ScrapeFailureException


def stub_converter(item):
    if item == ConvertFailureItem:
        raise ex.ConvertFailureException
    elif item == StubItem:
        return ConvertedItem
    else:
        return item


class StubPusher:
    def __init__(self):
        self._pushed_items = []

    def push(self, item):
        if item == PushFailureItem:
            raise ex.PushFailureException()
        else:
            self._pushed_items.append(item)

    def pushed_items(self):
        return self._pushed_items


class StubItem:
    pass


class ConvertedItem:
    pass


class ConvertFailureItem:
    pass


class PushFailureItem:
    pass


class ScrapeAndPushTest(unittest.TestCase):
    def setUp(self):
        self.pusher = StubPusher()

    def test__it_orchestrates_scraping_converting_and_pushing_activities(self):
        scraper = scraper_returning([StubItem, StubItem])

        event = sap.scrape_and_push(scrape=scraper, convert=stub_converter, push=self.pusher.push)
        event()

        self.assertEquals(self.pusher.pushed_items(), [ConvertedItem, ConvertedItem])

    def test__it_short_circuits_when_pushing_an_activity_fails(self):
        scraper = scraper_returning([StubItem, PushFailureItem])

        event = sap.scrape_and_push(scrape=scraper, convert=stub_converter, push=self.pusher.push)
        event()

        self.assertEquals(self.pusher.pushed_items(), [ConvertedItem])

    def test__it_short_circuits_when_converting_an_activity_fails(self):
        scraper = scraper_returning([StubItem, ConvertFailureItem])

        event = sap.scrape_and_push(scrape=scraper, convert=stub_converter, push=self.pusher.push)
        event()

        self.assertEquals(self.pusher.pushed_items(), [ConvertedItem])

    def test__it_short_circuits_when_scraping_fails(self):
        scraper = failing_scraper

        event = sap.scrape_and_push(scrape=scraper, convert=stub_converter, push=self.pusher.push)
        event()

        self.assertEquals(self.pusher.pushed_items(), [])
