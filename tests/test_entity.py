from mock import MagicMock
from pytest import raises


def test_actions_repr():
    from siren_client.entity import SirenActions
    sa = SirenActions(None, [{'name': 'do-it'}])
    assert str(sa) == '<SirenActions (do-it)>'


def test_action_repr():
    from siren_client.entity import SirenAction
    sa = SirenAction(None, {'name': 'do-it',
                            'fields': [{'name': 'field_one'}]})
    assert str(sa) == '<SirenAction (field_one)>'


def test_entities_repr():
    from siren_client.entity import SirenEntities
    se = SirenEntities(None, {})
    assert str(se) == '<SirenEntities (0)>'


def test_links_repr():
    client = MagicMock()
    client.convert_rel.return_value = 'link-one'
    from siren_client.entity import SirenLinks
    sl = SirenLinks(client, [{'rel': ['link-one'], 'href': 'nowhere'}])
    assert str(sl) == '<SirenLinks (link-one)>'


def test_entity_repr_empty():
    from siren_client.entity import SirenEntity
    se = SirenEntity(None, {})
    assert str(se) == '<SirenEntity (class:) (None)>'


def test_entity_repr_empty_refresh():
    from siren_client.entity import SirenEntity, SirenInvalid
    se = SirenEntity(None, {})
    with raises(SirenInvalid):
        se.refresh()


def test_entity_repr_self():
    from siren_client.client import SirenClient
    from siren_client.entity import SirenEntity
    se = SirenEntity(client=SirenClient(None),
                     data={'class': ['cool', 'medina'],
                           'links': [{'rel': ['self'],
                                      'href':'scifi://cool'}]})
    assert str(se) == "<SirenEntity (class:cool,medina) (scifi://cool)>"


def test_entity_non_unique_rels():
    client = MagicMock()
    client.convert_rel.return_value = 'link-one'
    from siren_client.entity import SirenLinks, SirenInvalid
    with raises(SirenInvalid) as error:
        sl = SirenLinks(client, [{'rel': ['link-one'], 'href': 'nowhere'},
                                 {'rel': ['link-one'], 'href': 'nowhere'}])


def test_entity_invalid_attribute():
    from siren_client.entity import SirenEntity
    se = SirenEntity(None, {})
    with raises(AttributeError):
        se.invalid
