import logging
import openahjo_activity_streams.exceptions as ex
import requests


def scrape_and_push(scrape, convert, push):
    def event():
        try:
            agenda_items = scrape()
            for item in agenda_items:
                activity = convert(item)
                push(activity)
        except (ex.PushFailureException, ex.ConvertFailureException, ex.ScrapeFailureException):
            pass

    return event


def scraper(coracle_endpoint, openahjo_endpoint):
    def scrape():
        coracle_timestamp_response = requests.get(coracle_endpoint)

        if coracle_timestamp_response.status_code != 200:
            raise ex.ScrapeFailureException

        latest_published_time = coracle_timestamp_response.json().get('latest-published-timestamp')
        if latest_published_time is not None:
            logging.info("successful request for latest_published_time " + str(latest_published_time))
        else:
            logging.info("no latest_published_time is returned")

        agenda_response = requests.get(openahjo_endpoint,
                                       params={'order_by': 'last_modified_time',
                                               'last_modified_time__gte': latest_published_time})

        if agenda_response.status_code != 200:
            raise ex.ScrapeFailureException

        agenda_items = agenda_response.json().get('objects')
        logging.info("scraped " + str(len(agenda_items)) + " items from OpenAhjo")
        return agenda_items

    return scrape


def pusher(coracle_endpoint, bearer_token):
    def push(item):
        response = requests.post(coracle_endpoint,
                                 json=item,
                                 headers={'bearer-token': bearer_token})

        if response.status_code != 201:
            logging.error("Pushing failed. Status code: " + str(response.status_code))
            raise ex.PushFailureException

    return push
