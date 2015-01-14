from pytest import fixture
import simplejson as json

REFERENCE_BODY = """
{
  "class": [ "order" ],
  "properties": {
      "orderNumber": 42,
      "itemCount": 3,
      "status": "pending"
  },
  "entities": [
    {
      "class": [ "items", "collection" ],
      "rel": [ "http://x.io/rels/order-items" ],
      "href": "http://api.x.io/orders/42/items"
    },
    {
      "class": [ "info", "customer" ],
      "rel": [ "http://x.io/rels/customer" ],
      "properties": {
        "customerId": "pj123",
        "name": "Peter Joseph"
      },
      "links": [
        { "rel": [ "self" ], "href": "http://api.x.io/customers/pj123" }
      ]
    }
  ],
  "actions": [
    {
      "name": "add-item",
      "title": "Add Item",
      "method": "POST",
      "href": "http://api.x.io/orders/42/items",
      "type": "application/x-www-form-urlencoded",
      "fields": [
        { "name": "orderNumber", "type": "hidden", "value": "42" },
        { "name": "productCode", "type": "text" },
        { "name": "quantity", "type": "number" }
      ]
    }
  ],
  "links": [
    { "rel": [ "self" ], "href": "http://api.x.io/orders/42" },
    { "rel": [ "previous" ], "href": "http://api.x.io/orders/41" },
    { "rel": [ "next" ], "href": "http://api.x.io/orders/43" }
  ]
}
"""


def siren_entity(data, **config):
    from siren_client.entity import SirenEntity
    from siren_client.client import SirenClient
    return SirenEntity(client=SirenClient(session=None, config=config),
                       data=data)


@fixture
def siren_reference():
    return siren_entity(json.loads(REFERENCE_BODY))


@fixture(params=['{}', REFERENCE_BODY])
def siren_traversal(request):
    return json.loads(request.param)


def test_empty_entity_attributes():
    entity = siren_entity({})
    assert entity.class_ == []
    assert entity.title is None
    assert entity.uri is None
    assert entity.rel is None
    assert entity.is_stub() is False
    assert entity.is_subentity() is False


def test_entity_traversal_objects(siren_traversal):
    from siren_client.entity import (
        SirenLinks,
        SirenActions,
        SirenEntities,
    )
    entity = siren_entity(siren_traversal)
    assert isinstance(entity.links, SirenLinks)
    assert isinstance(entity.actions, SirenActions)
    assert isinstance(entity.entities, SirenEntities)


def test_reference_entity(siren_reference):
    assert siren_reference.uri == "http://api.x.io/orders/42"
    assert siren_reference.is_stub() is False
    assert siren_reference.is_subentity() is False


def test_reference_class(siren_reference):
    assert siren_reference.class_ == ['order']


def test_reference_properties(siren_reference):
    assert siren_reference["orderNumber"] == 42
    assert siren_reference["itemCount"] == 3
    assert siren_reference["status"] == 'pending'


def test_reference_entities(siren_reference):
    assert len(siren_reference.entities) == 2

    entity = siren_reference.entities[0]
    # This is an embedded link subentity
    assert entity.uri == 'http://api.x.io/orders/42/items'
    assert entity.class_ == ['items', 'collection']
    assert entity.rel == ['http://x.io/rels/order-items']
    assert entity.is_subentity() is True
    assert entity.is_stub() is True

    entity = siren_reference.entities[1]
    # This is an embedded entity subentity
    assert entity.uri == 'http://api.x.io/customers/pj123'
    assert entity.class_ == ['info', 'customer']
    assert entity.rel == ['http://x.io/rels/customer']
    assert entity.is_subentity() is True
    assert entity.is_stub() is False


def test_reference_actions(siren_reference):
    assert len(siren_reference.actions) == 1
    assert 'add-item' in siren_reference.actions


def test_reference_links(siren_reference):
    assert len(siren_reference.links) == 3
    assert 'self' in siren_reference.links
    assert 'next' in siren_reference.links
    assert 'previous' in siren_reference.links


def test_reference_rel_shortening():
    siren_reference = siren_entity(json.loads(REFERENCE_BODY),
                                   rel_base='http://x.io/rels/')
    assert siren_reference.entities[0].rel == ['order-items']
    assert siren_reference.entities[1].rel == ['customer']
