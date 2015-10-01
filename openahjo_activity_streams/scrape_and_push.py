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

        agenda_response = requests.get(openahjo_endpoint,
                                       params={'order_by': 'last_modified_time',
                                               'last_modified_time__gte': latest_published_time})

        if agenda_response.status_code != 200:
            raise ex.ScrapeFailureException

        agenda_items = agenda_response.json().get('objects')

        return agenda_items

    return scrape
