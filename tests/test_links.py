from pytest import fixture
from mock import MagicMock

LINKS_PARENT = """
{
  "class": [ "test" ],
  "properties": { "Name": "Parent" },
  "links": [
    { "rel": [ "child-one" ], "href": "http://api.x.io/test/2" },
    { "rel": [ "child-two" ], "href": "http://api.x.io/test/3" },
    { "rel": [ "self" ], "href": "http://api.x.io/test/1" }
  ]
}
"""

LINKS_CHILD_ONE = """
{
  "class": [ "test" ],
  "properties": { "Name": "Child One" },
  "links": [ { "rel": [ "self" ], "href": "http://api.x.io/test/2" } ]
}
"""

LINKS_CHILD_TWO = """
{
  "class": [ "test" ],
  "properties": { "Name": "Child Two" },
  "links": [ { "rel": [ "self" ], "href": "http://api.x.io/test/3" } ]
}
"""


@fixture
def parent_entity():
    session = MagicMock(name='session')
    response = session.get.return_value
    response.content = LINKS_PARENT
    from siren_client import get
    return get('some_url', session=session)


def test_link_refresh():
    session = MagicMock(name='session')
    response = session.get.return_value
    response.content = LINKS_PARENT
    from siren_client import get

    siren_entity = get('some_url', session=session)
    assert str(siren_entity) == "<SirenEntity (class:test) " \
                                "(http://api.x.io/test/1)>"
    assert siren_entity.uri == 'http://api.x.io/test/1'
    assert siren_entity['Name'] == 'Parent'
    assert len(siren_entity.links) == 3
    response.content = LINKS_CHILD_ONE
    siren_entity.refresh()
    assert siren_entity.uri == 'http://api.x.io/test/2'
    assert siren_entity['Name'] == 'Child One'


def test_single_links_object(parent_entity):
    links_one = parent_entity.links
    links_two = parent_entity.links
    assert id(links_one) == id(links_two)


def test_link_child_one(parent_entity):
    response = parent_entity.client.session.get.return_value
    response.content = LINKS_CHILD_ONE

    child = parent_entity.links['child-one']
    assert child.uri == 'http://api.x.io/test/2'
    assert child['Name'] == 'Child One'


def test_link_child_two(parent_entity):
    response = parent_entity.client.session.get.return_value
    response.content = LINKS_CHILD_TWO

    child = parent_entity.links['child-two']
    assert child.uri == 'http://api.x.io/test/3'
    assert child['Name'] == 'Child Two'


def test_link_self(parent_entity):
    response = parent_entity.client.session.get.return_value

    child = parent_entity.links['self']
    assert child.uri == 'http://api.x.io/test/1'
    assert child['Name'] == 'Parent'
    assert id(child) != id(parent_entity)


def test_links_refetches(parent_entity):
    response = parent_entity.client.session.get.return_value
    response.content = LINKS_CHILD_ONE

    child_one = parent_entity.links['child-one']
    child_two = parent_entity.links['child-one']

    assert child_one['Name'] == 'Child One'
    assert child_two['Name'] == 'Child One'
    assert id(child_one) != id(child_two)
