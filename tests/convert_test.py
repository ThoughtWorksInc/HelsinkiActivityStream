# Copyright (c) 2015 ThoughtWorks
#
# See the file LICENSE for copying permission.

import unittest
import copy

from openahjo_activity_streams import convert
from tests.data.example_agenda_item import EXAMPLE_AGENDA_ITEM


class AgendaItemToActivityTest(unittest.TestCase):
    def setUp(self):
        super(AgendaItemToActivityTest, self).setUp()
        self._result = convert.agenda_item_to_activity(EXAMPLE_AGENDA_ITEM)

    def test_that_activity_type_is_Add(self):
        self.assertEquals(self._result['@type'], 'Add')


class AgendaItemToPublishedTest(unittest.TestCase):
    def test_that_published_is_correct_date_time_format(self):
        self._result = convert.agenda_item_to_published(EXAMPLE_AGENDA_ITEM)
        self.assertEquals(self._result, '2015-08-28T11:06:47.879Z')

    def test_that_published_is_correct_date_time_format_with_truncation_and_zero_padding(self):
        self._result = convert.agenda_item_to_published({"last_modified_time": "2015-08-28T11:06:47.005678"})
        self.assertEquals(self._result, '2015-08-28T11:06:47.005Z')


class AgendaItemToActorTest(unittest.TestCase):
    def setUp(self):
        super(AgendaItemToActorTest, self).setUp()
        self._result = convert.agenda_item_to_actor(EXAMPLE_AGENDA_ITEM)

    def test_that_actor_type_is_group(self):
        self.assertEquals(self._result['@type'], 'Group')

    def test_that_actor_id_generated_from_meeting_policymaker(self):
        expected = convert.OPENAHJO_BASE_URL + '/paatokset/v1/policymaker/11/'
        self.assertEquals(self._result['@id'], expected)

    def test_that_actor_display_name_comes_from_policymaker_name(self):
        self.assertEquals(self._result['displayName'],
                          EXAMPLE_AGENDA_ITEM['meeting']['policymaker_name'])


class AgendaItemToObjectWhenNoContentRecordsExist(unittest.TestCase):
    def test_that_content_is_empty(self):
        agenda_item_with_no_content = copy.deepcopy(EXAMPLE_AGENDA_ITEM)
        agenda_item_with_no_content['content'].clear()
        result = convert.agenda_item_to_object(agenda_item_with_no_content)
        self.assertEquals(result['content'], '')


class AgendaItemToObjectTest(unittest.TestCase):
    def setUp(self):
        super(AgendaItemToObjectTest, self).setUp()
        self._result = convert.agenda_item_to_object(EXAMPLE_AGENDA_ITEM)

    def test_that_object_type_is_content(self):
        self.assertEquals(self._result['@type'], 'Content')

    def test_that_object_id_generated_from_agenda_item_resource_uri(self):
        expected = convert.OPENAHJO_BASE_URL + \
                   '/paatokset/v1/agenda_item/51427/'
        self.assertEquals(self._result['@id'], expected)

    def test_that_object_display_name_comes_from_subject(self):
        self.assertEquals(self._result['displayName'],
                          EXAMPLE_AGENDA_ITEM['subject'])

    def test_that_object_url_comes_from_agenda_item_permalink(self):
        self.assertEquals(self._result['url'],
                          EXAMPLE_AGENDA_ITEM['permalink'])

    def test_that_object_content_comes_from_first_agend_item_content_text_property(self):
        self.assertEquals(self._result['content'],
                          EXAMPLE_AGENDA_ITEM['content'][0]['text'])


class AgendaItemToTargetTest(unittest.TestCase):
    def setUp(self):
        super(AgendaItemToTargetTest, self).setUp()
        self._result = convert.agenda_item_to_target(EXAMPLE_AGENDA_ITEM)

    def test_that_target_type_is_content(self):
        self.assertEquals(self._result['@type'], 'Content')

    def test_that_target_id_is_generated_from_issue_resource_uri(self):
        expected = convert.OPENAHJO_BASE_URL + '/paatokset/v1/issue/20995/'
        self.assertEquals(self._result['@id'], expected)

    def test_that_target_display_name_comes_from_the_issue_subject(self):
        self.assertEquals(self._result['displayName'],
                          EXAMPLE_AGENDA_ITEM['issue']['subject'])

    def test_that_target_content_comes_from_the_issue_summary(self):
        self.assertEquals(self._result['content'],
                          EXAMPLE_AGENDA_ITEM['issue']['summary'])


class AgendaItemToTargetWhenNoIssueSummaryTest(unittest.TestCase):

    def test_that_target_content_is_empty(self):
        agenda_item_without_issue_summary = copy.deepcopy(EXAMPLE_AGENDA_ITEM)
        agenda_item_without_issue_summary['issue'].pop('summary')
        result = convert.agenda_item_to_target(agenda_item_without_issue_summary)
        self.assertEquals(result['content'], '')


class ToActivityStreamTest(unittest.TestCase):

    def test_that_agenda_items_are_converted_to_activities(self):
        result = convert.to_activity_stream({'objects': [EXAMPLE_AGENDA_ITEM]})
        self.assertEquals(result,
                          [convert.agenda_item_to_activity(EXAMPLE_AGENDA_ITEM)])
