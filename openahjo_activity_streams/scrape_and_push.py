def scrape_and_push(scrape, convert, push):
    def event():
        agenda_items = scrape()
        for item in agenda_items:
            activity = convert(item)
            push(activity)

    return event
