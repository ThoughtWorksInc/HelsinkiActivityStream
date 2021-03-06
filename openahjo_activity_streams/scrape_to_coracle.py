import logging
import os
import flask
from openahjo_activity_streams import convert
from openahjo_activity_streams.scheduler import Clock
from openahjo_activity_streams.scheduler import Scheduler
from openahjo_activity_streams.scrape_and_push import scraper, pusher, scrape_and_push


def create_scheduler():
    logging.basicConfig(level=logging.INFO)
    application = flask.Flask(__name__)
    coracle_timestamp_endpoint = os.environ['CORACLE_TIMESTAMP_ENDPOINT']
    coracle_post_activity_endpoint = os.environ['CORACLE_POST_ACTIVITY_ENDPOINT']
    openahjo_endpoint = os.environ['OPENAHJO_ENDPOINT']
    bearer_token = os.environ['BEARER_TOKEN']

    scrape = scraper(coracle_timestamp_endpoint, openahjo_endpoint)
    push = pusher(coracle_post_activity_endpoint, bearer_token)

    logging.basicConfig(level=logging.INFO)
    scrape_and_push_event_loop = scrape_and_push(scrape=scrape,
                                                 convert=convert.agenda_item_to_activity,
                                                 push=push)
    clock = Clock()
    s = Scheduler(interval=3600, clock=clock, stop_when=lambda: False, event=scrape_and_push_event_loop)
    s.start()

    return application


application = create_scheduler()
if __name__ == '__main__':
    application.run()
