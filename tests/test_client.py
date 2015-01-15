from pytest import fixture, raises
from mock import MagicMock


def get_siren_client(**kwargs):
    from siren_client import SirenClient
    if 'session' not in kwargs:
        kwargs['session'] = None
    return SirenClient(**kwargs)


def test_config_override():
    config = {
        'self_rel': 'mep',
    }
    sc = get_siren_client(session=None, config=config)
    assert sc.config['self_rel'] == 'mep'
    assert sc.config['rel_base'] is None


def test_config_addition():
    config = {
        'foo': 'bar',
    }
    sc = get_siren_client(session=None, config=config)
    assert sc.config['self_rel'] == 'self'
    assert sc.config['rel_base'] is None
    assert sc.config['foo'] == 'bar'


def test_request():
    session = MagicMock(name='session')
    response = session.get.return_value
    response.content = '{}'
    sc = get_siren_client(session=session)

    sc.request('some_url')
    response.raise_for_status.assert_called_with()
    session.get.assert_called_once_with('some_url')


def test_request_extra_params():
    session = MagicMock(name='session')
    response = session.get.return_value
    response.content = '{}'
    sc = get_siren_client(session=session)

    sc.request('some_url', foo='bar')
    session.get.assert_called_once_with('some_url', foo='bar')


def test_request_alternate_method():
    session = MagicMock(name='session')
    response = session.foobar.return_value
    response.content = '{}'
    sc = get_siren_client(session=session)

    sc.request('some_url', method='foobar')
    session.foobar.assert_called_once_with('some_url')


def test_request_invalid_json():
    session = MagicMock(name='session')
    response = session.get.return_value
    response.content = ''
    response.headers = {'content-type': 'application/json'}
    sc = get_siren_client(session=session)

    from simplejson import JSONDecodeError
    with raises(JSONDecodeError):
        sc.request('some_url')


def test_request_default_invalid_json():
    session = MagicMock(name='session')
    response = session.get.return_value
    response.content = 'Jibo'
    sc = get_siren_client(session=session)

    response = sc.request('some_url')
    assert response == 'Jibo'


def test_follow():
    sc = get_siren_client()
    sc.request = MagicMock(name='request', return_value={})

    from siren_client.entity import SirenEntity
    se = sc.follow('some_other_url')
    assert isinstance(se, SirenEntity)
    sc.request.assert_called_once_with('some_other_url', method='get')


def test_follow_extra_args():
    from siren_client.entity import SirenEntity
    sc = get_siren_client()
    sc.request = MagicMock(name='request', return_value={})

    se = sc.follow('some_other_url', foo='bar')
    assert isinstance(se, SirenEntity)
    sc.request.assert_called_once_with('some_other_url',
                                       method='get',
                                       foo='bar')


def test_loads_override():
    session = MagicMock(name='session')
    session.get.return_value.content = 'Super Response'
    session.get.return_value.headers = {}

    my_loads = MagicMock(name='my_loads')
    config = dict(loads=my_loads)
    sc = get_siren_client(session=session, config=config)

    sc.request('some_url')
    my_loads.assert_called_with(None, 'Super Response')


def test_dumps_override():
    session = MagicMock(name='session')
    session.get.return_value.content = '{}'

    my_dumps = MagicMock(name='my_dumps')
    config = dict(dumps=my_dumps)
    sc = get_siren_client(session=session, config=config)

    sc.request('some_url', data='My Awesome Data')
    my_dumps.assert_called_with(None, 'My Awesome Data')


def test_convert_rel():
    sc = get_siren_client(config={'rel_base': 'super'})
    assert sc.convert_rel('some_rel') == 'some_rel'
    assert sc.convert_rel('supersome_rel') == 'some_rel'
    assert sc.convert_rel('super/some_rel') == '/some_rel'
    assert sc.convert_rel('/super/some_rel') == '/super/some_rel'

    sc = get_siren_client()
    assert sc.convert_rel('some_rel') == 'some_rel'
    assert sc.convert_rel('supersome_rel') == 'supersome_rel'
    assert sc.convert_rel('/super/some_rel') == '/super/some_rel'

    sc = get_siren_client(config={'rel_base': '/super/'})
    assert sc.convert_rel('some_rel') == 'some_rel'
    assert sc.convert_rel('supersome_rel') == 'supersome_rel'
    assert sc.convert_rel('/super/some_rel') == 'some_rel'
