import unittest

from openahjo_activity_streams import convert
from tests.data.example_agenda_item import STUB_AGENDA_ITEM


class AgendaItemToActivityTest(unittest.TestCase):
    def setUp(self):
        super(AgendaItemToActivityTest, self).setUp()
        self._result = convert.agenda_item_to_activity(STUB_AGENDA_ITEM)

    def test_that_activity_type_is_Add(self):
        self.assertEquals(self._result['@type'], 'Add')


class AgendaItemToActorTest(unittest.TestCase):
    def setUp(self):
        super(AgendaItemToActorTest, self).setUp()
        self._result = convert.agenda_item_to_actor(STUB_AGENDA_ITEM)

    def test_that_actor_type_is_group(self):
        self.assertEquals(self._result['@type'], 'Group')

    def test_that_actor_id_generated_from_meeting_policymaker(self):
        expected = convert.OPENAHJO_BASE_URL + '/paatokset/v1/policymaker/11/'
        self.assertEquals(self._result['@id'], expected)

    def test_that_actor_display_name_comes_from_policymaker_name(self):
        self.assertEquals(self._result['displayName'],
                          STUB_AGENDA_ITEM['meeting']['policymaker_name'])


class AgendaItemToObjectTest(unittest.TestCase):
    def setUp(self):
        super(AgendaItemToObjectTest, self).setUp()
        self._result = convert.agenda_item_to_object(STUB_AGENDA_ITEM)

    def test_that_object_type_is_content(self):
        self.assertEquals(self._result['@type'], 'Content')

    def test_that_object_id_generated_from_agenda_item_resource_uri(self):
        expected = convert.OPENAHJO_BASE_URL + \
                   '/paatokset/v1/agenda_item/51427/'
        self.assertEquals(self._result['@id'], expected)

    def test_that_object_display_name_comes_from_subject(self):
        self.assertEquals(self._result['displayName'],
                          STUB_AGENDA_ITEM['subject'])

    def test_that_object_url_comes_from_agenda_item_permalink(self):
        self.assertEquals(self._result['url'],
                          STUB_AGENDA_ITEM['permalink'])


class AgendaItemToTargetTest(unittest.TestCase):
    def setUp(self):
        super(AgendaItemToTargetTest, self).setUp()
        self._result = convert.agenda_item_to_target(STUB_AGENDA_ITEM)

    def test_that_target_type_is_content(self):
        self.assertEquals(self._result['@type'], 'Content')

    def test_that_target_id_is_generated_from_issue_resource_uri(self):
        expected = convert.OPENAHJO_BASE_URL + '/paatokset/v1/issue/20995/'
        self.assertEquals(self._result['@id'], expected)

    def test_that_target_display_name_comes_from_the_issue_subject(self):
        self.assertEquals(self._result['displayName'],
                          STUB_AGENDA_ITEM['issue']['subject'])


class ToActivityStreamTest(unittest.TestCase):
    def test_that_result_has_envelope_headers(self):
        result = convert.to_activity_stream({})
        self.assertEquals(result,
                          {'@context': 'http://www.w3.org/ns/activitystreams',
                           '@type': 'OrderedCollection',
                           'orderedItems': []})

    def test_that_agenda_items_are_converted_to_activities(self):
        result = convert.to_activity_stream({'objects': [STUB_AGENDA_ITEM]})
        self.assertEquals(result['orderedItems'],
                          [convert.agenda_item_to_activity(STUB_AGENDA_ITEM)])
