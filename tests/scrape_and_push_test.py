# Copyright (c) 2015 ThoughtWorks
#
# See the file LICENSE for copying permission.
import json
import unittest
import openahjo_activity_streams.exceptions as ex
import openahjo_activity_streams.scrape_and_push as sap
import responses


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


class ScraperTest(unittest.TestCase):
    def setUp(self):
        self.coracle_timestamp_endpoint = 'http://coracle.endpoint.org/latest-published-timestamp'
        self.coracle_timestamp_response_body = '{"latest-published-timestamp": "2015-09-01T00:00:00.000Z"}'
        self.openahjo_endpoint = 'http://openahjo.endpoint.org/agenda_item/'
        self.openahjo_response_body = """{"meta":{"limit": 20,
                                      "next": null,
                                      "offset": 0,
                                      "previous": null,
                                      "total_count": 0},
                              "objects": [{"Object": "123"}]}"""
        self.last_modified_time = 'last_modified_time__gte=2015-09-01T00%3A00%3A00.000Z'
        self.order_by = 'order_by=last_modified_time'

    def test__scrapes_source_endpoint_for_new_data(self):
        query_string = '?' + self.last_modified_time + '&' + self.order_by
        openahjo_endpoint_with_query_string = self.openahjo_endpoint + query_string

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.coracle_timestamp_endpoint,
                     body=self.coracle_timestamp_response_body, status=200,
                     content_type="application/json")
            rsps.add(responses.GET, openahjo_endpoint_with_query_string,
                     body=self.openahjo_response_body, status=200,
                     content_type="application/json",
                     match_querystring=True)

            scrape = sap.scraper(coracle_endpoint=self.coracle_timestamp_endpoint,
                                 openahjo_endpoint=self.openahjo_endpoint)
            agenda_items = scrape()

            self.assertEquals(agenda_items, [{'Object': '123'}])

    def test__scrapes_source_endpoint_without_last_modified_time_if_no_time_is_returned_by_coracle(self):
        query_string = '?' + self.order_by
        openahjo_endpoint_with_query_string = self.openahjo_endpoint + query_string

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.coracle_timestamp_endpoint,
                     body="{}", status=200,
                     content_type="application/json")
            rsps.add(responses.GET, openahjo_endpoint_with_query_string,
                     body=self.openahjo_response_body, status=200,
                     content_type="application/json",
                     match_querystring=True)

            scrape = sap.scraper(coracle_endpoint=self.coracle_timestamp_endpoint,
                                 openahjo_endpoint=self.openahjo_endpoint)
            agenda_items = scrape()
            self.assertEquals(agenda_items, [{'Object': '123'}])

    def test__raises_ScraperFailureException_when_GET_on_coracle_endpoint_fails(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.coracle_timestamp_endpoint,
                     status=500)

            scrape = sap.scraper(coracle_endpoint=self.coracle_timestamp_endpoint,
                                 openahjo_endpoint=self.openahjo_endpoint)

            self.assertRaises(ex.ScrapeFailureException, scrape)

    def test__raises_ScraperFailureException_when_GET_on_openahjo_endpoint_fails(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.coracle_timestamp_endpoint,
                     body=self.coracle_timestamp_response_body, status=200,
                     content_type="application/json")
            rsps.add(responses.GET, self.openahjo_endpoint,
                     status=500)

            scrape = sap.scraper(coracle_endpoint=self.coracle_timestamp_endpoint,
                                 openahjo_endpoint=self.openahjo_endpoint)

            self.assertRaises(ex.ScrapeFailureException, scrape)


class PusherTest(unittest.TestCase):
    def setUp(self):
        self.coracle_post_activity_endpoint = 'http://coracle.endpoint.org/add-activity'
        self.coracle_bearer_token = 'secret'

    def test__pushes_activity_to_coracle(self):
        item = {'@type': 'Create'}
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, self.coracle_post_activity_endpoint,
                     status=201)

            push = sap.pusher(coracle_endpoint=self.coracle_post_activity_endpoint,
                              bearer_token=self.coracle_bearer_token)
            push(item)

            self.assertEquals(json.loads(rsps.calls[0].request.body), item)

    def test__sets_bearer_token_in_POST_request(self):
        item = {'@type': 'Create'}
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, self.coracle_post_activity_endpoint,
                     status=201)

            push = sap.pusher(coracle_endpoint=self.coracle_post_activity_endpoint,
                              bearer_token=self.coracle_bearer_token)
            push(item)

            self.assertEquals(rsps.calls[0].request.headers.get('bearer-token'), self.coracle_bearer_token)

    def test__raises_PushFailureException_when_POST_to_coracle_endpoint_fails(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, self.coracle_post_activity_endpoint,
                     status=500)

            push = sap.pusher(coracle_endpoint=self.coracle_post_activity_endpoint,
                              bearer_token=self.coracle_bearer_token)

            self.assertRaises(ex.PushFailureException, push, {})
