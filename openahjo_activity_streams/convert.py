# Copyright (c) 2015 ThoughtWorks
#
# See the file LICENSE for copying permission.
from datetime import datetime
from pytz import timezone

OPENAHJO_BASE_URL = 'http://dev.hel.fi'
OPENAHJO_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
OPENAHJO_TIME_ZONE = 'Europe/Helsinki'


def resolve_url(path):
    return OPENAHJO_BASE_URL + path


def agenda_item_to_actor(agenda_item):
    meeting = agenda_item['meeting']
    return {
        'type': 'Group',
        'id': resolve_url(meeting['policymaker']),
        'name': meeting['policymaker_name'],
    }


def agenda_item_to_object(agenda_item):
    return {
        'type': 'Content',
        'id': resolve_url(agenda_item['resource_uri']),
        'url': agenda_item['permalink'],
        'name': agenda_item['subject'],
        'content': get_content_text(agenda_item),
    }


def get_content_text(agenda_item):
    return agenda_item['content'][0]['text'] if agenda_item['content'] else ''


def agenda_item_to_target(agenda_item):
    issue = agenda_item['issue']
    return {
        'type': 'Content',
        'id': resolve_url(issue['resource_uri']),
        'name': issue['subject'],
        'content': issue.get('summary', ''),
    }


def agenda_item_to_published(agenda_item):
    datetime_object = datetime.strptime(agenda_item['last_modified_time'], OPENAHJO_DATE_FORMAT)
    datetime_object_without_microseconds = datetime_object.replace(microsecond=0)
    datetime_in_tz = timezone(OPENAHJO_TIME_ZONE).localize(datetime_object_without_microseconds)
    return datetime_in_tz.isoformat()


def agenda_item_to_activity(agenda_item):
    return {
        '@context': 'http://www.w3.org/ns/activitystreams',
        'type': 'Add',
        'published': agenda_item_to_published(agenda_item),
        'actor': agenda_item_to_actor(agenda_item),
        'object': agenda_item_to_object(agenda_item),
        'target': agenda_item_to_target(agenda_item),
    }


def to_activity_stream(openahjo_data):
    return [agenda_item_to_activity(item)
            for item in openahjo_data.get('objects', [])]


def identity_converter(openahjo_data):
    return openahjo_data
