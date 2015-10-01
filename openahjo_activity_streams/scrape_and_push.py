import openahjo_activity_streams.exceptions as ex


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
