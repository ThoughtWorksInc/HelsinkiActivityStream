OPENAHJO_BASE_URL = 'http://dev.hel.fi'


def resolve_url(path):
    return OPENAHJO_BASE_URL + path


def agenda_item_to_actor(agenda_item):
    meeting = agenda_item['meeting']
    return {
        '@type': 'Group',
        '@id': resolve_url(meeting['policymaker']),
        'displayName': meeting['policymaker_name'],
    }


def agenda_item_to_object(agenda_item):
    return {
        '@type': 'Content',
        '@id': resolve_url(agenda_item['resource_uri']),
        'url': agenda_item['permalink'],
        'displayName': agenda_item['subject'],
        '??content': '??>>',
    }


def agenda_item_to_target(agenda_item):
    issue = agenda_item['issue']
    return {
        '@type': 'Content',
        '@id': resolve_url(issue['resource_uri']),
        'displayName': issue['subject'],
        '??content': '????',
    }


def agenda_item_to_activity(agenda_item):
    return {
        '@context': 'http://www.w3.org/ns/activitystreams',
        '@type': 'Add',
        'published': agenda_item['last_modified_time'],
        'actor': agenda_item_to_actor(agenda_item),
        'object': agenda_item_to_object(agenda_item),
        'target': agenda_item_to_target(agenda_item),
    }


def to_activity_stream(openahjo_data):
    return {'@context': 'http://www.w3.org/ns/activitystreams',
            '@type': 'OrderedCollection',
            'orderedItems': []}


def identity_converter(openahjo_data):
    return openahjo_data