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
        latest_published_time = requests.get(coracle_endpoint).json().get('latest-published-timestamp')
        agenda_response = requests.get(openahjo_endpoint,
                                       params={'order_by': 'last_modified_time',
                                               'last_modified_time__gte': latest_published_time})
        agenda_items = agenda_response.json().get('objects')

        return agenda_items

    return scrape
