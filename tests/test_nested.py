from py.test import fixture

SCENARIOS = []

SCENARIOS.append({
    'source': [{'name': 'name', 'type': 'text' }],
    'result': [{'name': 'name', 'type': 'text'}]
})

SCENARIOS.append({
    'source': [{'name': 'name', 'type': 'text',},
               {'name': 'second', 'type': 'number',},
              ],
    'result': [{'name': 'name', 'type': 'text'},
               {'name': 'second', 'type': 'number'},
              ]
})

SCENARIOS.append({
    'source': [{'name': 'email', 'type': 'email',},
               {'name': 'email', 'type': 'email',},
              ],
    'result': [{'name': 'email[0]', 'type': 'email'},
               {'name': 'email[1]', 'type': 'email'},
              ]
})

SCENARIOS.append({
    'source': [{'name': 'address[street]', 'type': 'text' },
               {'name': 'address[city]', 'type': 'number' }
              ],
    'result': [{'name': 'address', 'type': 'nested.single',
                'nested' : [{ 'name': 'street', 'type': 'text' },
                            { 'name': 'city', 'type': 'number' }]}
              ]
})

SCENARIOS.append({
    'source': [{'name': '[][href]', 'type': 'text',},
               {'name': '[][rel]', 'type': 'text',},
              ],
    'result': [{'name': '', 'type': 'nested.multiple',
                'nested' : [{ 'name': 'href', 'type': 'text' },
                            { 'name': 'rel', 'type': 'text' }]},
              ],
})


SCENARIOS.append({
    'source': [{'name': 'address[][street]', 'type': 'text' },
               {'name': 'address[][number]', 'type': 'number' }
              ],
    'result': [{'name': 'address', 'type': 'nested.multiple',
                'nested' : [{ 'name': 'street', 'type': 'text' },
                            { 'name': 'number', 'type': 'number' }]}
              ]
})


SCENARIOS.append({
    'source': [{'name': 'name', 'type': 'text', 'required': 'true' },
               {'name': 'address[street]', 'type': 'text' },
               {'name': 'address[number]', 'type': 'number' },
               {'name': 'emails[][email]', 'type': 'email' },
               {'name': 'emails[][type]', 'type': 'text' },
              ],
    'result': [{'name': 'name', 'type': 'text', 'required': 'true'},
               {'name': 'address', 'type': 'nested.single',
                'nested' : [{ 'name': 'street', 'type': 'text' },
                            { 'name': 'number', 'type': 'number' }]},
               {'name': 'emails', 'type': 'nested.multiple',
                'nested' : [{ 'name': 'email', 'type': 'email' },
                            { 'name': 'type', 'type': 'text' }]}
              ]
})


SCENARIOS.append({
    'source': [{'name': 'name', 'type': 'text', 'required': 'true' },
               {'name': 'friends[][name]', 'type': 'text' },
               {'name': 'friends[][email]', 'type': 'email' },
               {'name': 'friends[][email]', 'type': 'email' },
              ],
    'result': [
                {'name': 'name', 'required': 'true', 'type': 'text'},
                {'name': 'friends',
                 'type': 'nested.multiple',
                 'nested': [
                        {'name': 'name', 'type': 'text'},
                        {'name': 'email[0]', 'type': 'email'},
                        {'name': 'email[1]', 'type': 'email'},
                     ]}]
})


SCENARIOS.append({
    'source': [{'name': 'name', 'type': 'text', 'required': 'true' },
               {'name': 'friends[][email][][email]', 'type': 'email' },
              ],
    'result': [
                {'name': 'name', 'required': 'true', 'type': 'text'},
                {'name': 'friends',
                 'type': 'nested.multiple',
                 'nested': [
                    {'name': 'email',
                     'type': 'nested.multiple',
                     'nested': [
                        {'name': 'email', 'type': 'email'},
                     ]}]}]
})


SCENARIOS.append({
    'source': [{'name': 'name', 'type': 'text', 'required': 'true' },
               {'name': 'address[street]', 'type': 'text' },
               {'name': 'address[number]', 'type': 'number' },
               {'name': 'emails[][email]', 'type': 'email' },
               {'name': 'emails[][type]', 'type': 'text' },
               {'name': 'friends[][emails][][email]', 'type': 'email' },
               {'name': 'friends[][emails][][type]', 'type': 'text' },
              ],
    'result': [{'name': 'name', 'type': 'text', 'required': 'true'},
               {'name': 'address', 'type': 'nested.single',
                'nested' : [{ 'name': 'street', 'type': 'text' },
                            { 'name': 'number', 'type': 'number' }]},
               {'name': 'emails', 'type': 'nested.multiple',
                'nested' : [{ 'name': 'email', 'type': 'email' },
                            { 'name': 'type', 'type': 'text' }]},
               {'name': 'friends', 'type': 'nested.multiple',
                'nested' : [{
                    'name': 'emails', 'type': 'nested.multiple',
                    'nested': [
                        { 'name': 'email', 'type': 'email' },
                        { 'name': 'type', 'type': 'text' }]}
              ]},
              ]
})

SCENARIOS.append({
    'source': [{'name': 'name', 'type': 'text', 'required': 'true' },
               {'name': 'address[street]', 'type': 'text' },
               {'name': 'address[number]', 'type': 'number' },
               {'name': 'emails[][email]', 'type': 'email' },
               {'name': 'emails[][type]', 'type': 'text' },
               {'name': 'friends[][address][street]', 'type': 'email' },
               {'name': 'friends[][address][number]', 'type': 'text' },
              ],
    'result': [{'name': 'name', 'required': 'true', 'type': 'text'},
               {'name': 'address',
                'nested': [{'name': 'street', 'type': 'text'},
                           {'name': 'number', 'type': 'number'}],
                'type': 'nested.single'},
               {'name': 'emails',
                'nested': [{'name': 'email', 'type': 'email'},
                           {'name': 'type', 'type': 'text'}],
                'type': 'nested.multiple'},
               {'name': 'friends',
                'nested': [{'name': 'address',
                            'nested': [{'name': 'street', 'type': 'email'},
                                       {'name': 'number', 'type': 'text'}],
                            'type': 'nested.single'}],
                'type': 'nested.multiple'}]
                })

SCENARIOS.append({
    'source': [{'name': 'name', 'type': 'text', 'required': 'true' },
               {'name': 'address[street]', 'type': 'text' },
               {'name': 'address[number]', 'type': 'number' },
               {'name': 'emails[][email]', 'type': 'email' },
               {'name': 'emails[][type]', 'type': 'text' },
               {'name': 'friends[][address][street]', 'type': 'email' },
               {'name': 'friends[][address][number]', 'type': 'text' },
               {'name': 'friends[][emails][][email]', 'type': 'email' },
               {'name': 'friends[][emails][][type]', 'type': 'text' },
              ],
    'result': [{'name': 'name', 'required': 'true', 'type': 'text'},
               {'name': 'address',
                'nested': [{'name': 'street', 'type': 'text'},
                           {'name': 'number', 'type': 'number'}],
                'type': 'nested.single'},
               {'name': 'emails',
                'nested': [{'name': 'email', 'type': 'email'},
                           {'name': 'type', 'type': 'text'}],
                'type': 'nested.multiple'},
               {'name': 'friends',
                'nested': [{'name': 'address',
                            'nested': [{'name': 'street', 'type': 'email'},
                                       {'name': 'number', 'type': 'text'}],
                            'type': 'nested.single'},
                           {'name': 'emails',
                            'nested': [{'name': 'email', 'type': 'email'},
                                       {'name': 'type', 'type': 'text'}],
                            'type': 'nested.multiple'}],
                'type': 'nested.multiple'}],
})


@fixture(params=SCENARIOS)
def field_data(request):
    return request.param


def test_transform(field_data):
    from siren_client.nested import transform
    result = transform(field_data['source'])
    assert result == field_data['result']


