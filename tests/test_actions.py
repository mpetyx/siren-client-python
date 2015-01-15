from pytest import fixture
from mock import MagicMock

ACTION_PARENT = """
{
  "class": [ "test" ],
  "properties": { "Name": "Parent" },
  "actions": [
    {
      "name": "action-one",
      "method": "GET",
      "href": "http://api.x.io/actions/one",
      "type": "application/x-www-form-urlencoded",
      "fields": [
        { "name": "Name", "type": "text" },
        { "name": "id", "type": "number", "value": "23" }
      ]
    },
    {
      "name": "action-two",
      "method": "GET",
      "href": "http://api.x.io/actions/two",
      "type": "application/json",
      "fields": [
        { "name": "Name", "type": "text" },
        { "name": "id", "type": "number", "value": "23" }
      ]
    },
    {
      "name": "action-three",
      "method": "POST",
      "href": "http://api.x.io/actions/three",
      "type": "application/x-www-form-urlencoded",
      "fields": [
        { "name": "Name", "type": "text" },
        { "name": "id", "type": "number", "value": "23" }
      ]
    },
    {
      "name": "action-four",
      "method": "POST",
      "href": "http://api.x.io/actions/four",
      "type": "application/json",
      "fields": [
        { "name": "Name", "type": "text" },
        { "name": "id", "type": "number", "value": "23" }
      ]
    },
    {
      "name": "action-five",
      "method": "funky",
      "href": "http://api.x.io/actions/five",
      "type": "application/json",
      "fields": [
        { "name": "Name", "type": "text" },
        { "name": "id", "type": "number", "value": "23" }
      ]
    },
    {
      "name": "action-six",
      "method": "POST",
      "href": "http://api.x.io/actions/six"
    },
    {
      "name": "action-seven",
      "href": "http://api.x.io/actions/seven"
    }
  ]
}
"""

ACTION_RESPONSE = """
{
  "class": [ "action-response" ],
  "properties": { "Name": "Response It." },
  "links": [ { "rel": [ "self" ], "href": "http://api.x.io/supers/1" } ]
}
"""


@fixture
def parent_entity():
    session = MagicMock(name='session')
    response = session.get.return_value
    response.content = ACTION_PARENT

    from siren_client import get
    parent = get('some_url', session=session)
    response.content = ACTION_RESPONSE
    return parent


def test_parent(parent_entity):
    assert len(parent_entity.actions) == 7


def test_actions_object_singular(parent_entity):
    actions_one = parent_entity.actions
    actions_two = parent_entity.actions
    assert id(actions_one) == id(actions_two)


def test_action_object_singular(parent_entity):
    action_one = parent_entity.actions['action-one']
    action_two = parent_entity.actions['action-one']
    assert id(action_one) == id(action_two)


def test_action_one(parent_entity):
    session = parent_entity.client.session
    response = parent_entity.actions['action-one']()

    assert response['Name'] == 'Response It.'
    session.get.assert_called_with("http://api.x.io/actions/one",
                                   data=None,
                                   params={'id': '23'})


def test_action_two(parent_entity):
    session = parent_entity.client.session
    response = parent_entity.actions['action-two'](Name='SomeName')

    assert response['Name'] == 'Response It.'
    session.get.assert_called_with("http://api.x.io/actions/two",
                                   data=None,
                                   params={'Name': 'SomeName',
                                           'id': '23'})


def test_action_three(parent_entity):
    session = parent_entity.client.session
    session.post.return_value.content = ACTION_RESPONSE
    response = parent_entity.actions['action-three'](Name='SomeName')

    assert response['Name'] == 'Response It.'
    session.post.assert_called_with(
        "http://api.x.io/actions/three",
        data={'id': '23', 'Name': 'SomeName'},
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )


def test_action_four(parent_entity):
    session = parent_entity.client.session
    session.post.return_value.content = ACTION_RESPONSE
    response = parent_entity.actions['action-four'](Name='SomeName')

    assert response['Name'] == 'Response It.'
    session.post.assert_called_with(
        "http://api.x.io/actions/four",
        data='{"id": "23", "Name": "SomeName"}',
        headers={'content-type': 'application/json'}
    )


def test_action_five(parent_entity):
    session = parent_entity.client.session
    session.funky.return_value.content = ACTION_RESPONSE
    response = parent_entity.actions['action-five'](Name='SomeName')

    assert response['Name'] == 'Response It.'
    session.funky.assert_called_with(
        "http://api.x.io/actions/five",
        data='{"id": "23", "Name": "SomeName"}',
        headers={'content-type': 'application/json'}
    )


def test_action_six(parent_entity):
    session = parent_entity.client.session
    session.post.return_value.content = ACTION_RESPONSE
    response = parent_entity.actions['action-six'](Name='SomeName')

    assert response['Name'] == 'Response It.'
    session.post.assert_called_with(
        "http://api.x.io/actions/six",
        data={'Name': 'SomeName'},
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )


def test_action_seven(parent_entity):
    session = parent_entity.client.session
    response = parent_entity.actions['action-seven'](Name='SomeName')

    assert response['Name'] == 'Response It.'
    session.get.assert_called_with("http://api.x.io/actions/seven",
                                   params={'Name': 'SomeName'},
                                   data=None)


def test_populate_action_one(parent_entity):
    session = parent_entity.client.session
    parent_entity.actions['action-one'].populate(parent_entity)
    response = parent_entity.actions['action-one'](id=4)

    assert response['Name'] == 'Response It.'
    session.get.assert_called_with("http://api.x.io/actions/one",
                                   data=None,
                                   params={'Name': 'Parent', 'id': 4})


def test_populate_action_three(parent_entity):
    session = parent_entity.client.session
    session.post.return_value.content = ACTION_RESPONSE
    parent_entity.actions['action-three'].populate(parent_entity)
    response = parent_entity.actions['action-three'](desc='A Desc')

    assert response['Name'] == 'Response It.'
    session.post.assert_called_with(
        "http://api.x.io/actions/three",
        data={'id': '23', 'desc': 'A Desc', 'Name': 'Parent'},
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )


def test_populate_action_six(parent_entity):
    session = parent_entity.client.session
    session.post.return_value.content = ACTION_RESPONSE
    parent_entity.actions['action-six'].populate(parent_entity)
    response = parent_entity.actions['action-six'](desc='A Desc')

    assert response['Name'] == 'Response It.'
    session.post.assert_called_with(
        "http://api.x.io/actions/six",
        data={'desc': 'A Desc'},
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )


def test_populate_action_seven(parent_entity):
    session = parent_entity.client.session
    parent_entity.actions['action-seven'].populate(parent_entity)
    response = parent_entity.actions['action-seven'](desc='Some Desc')

    assert response['Name'] == 'Response It.'
    session.get.assert_called_with(
        "http://api.x.io/actions/seven",
        params={'desc': 'Some Desc'},
        data=None
    )
