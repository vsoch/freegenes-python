'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from freegenes.main import Client
import shutil
import os


def _list_and_single(func):
    '''for a given endpoint that returns a list and a single view, 
       ensure that the list works to return 200 (and a list of results),
       and if we have a result, also query for a single entity. This is a
       simple test that just ensures that the endpoints are functioning.
    '''
    print('Testing %s' % func.__name__)
    results = func()
    assert isinstance(results, list)

    if len(results) > 0:
        result = func(uuid=results[0]['uuid'])
        assert isinstance(result, dict)
        assert "uuid" in result
        assert result['uuid'] == results[0]['uuid']


def test_endpoints():

    client = Client()
    _list_and_single(client.get_authors)
    _list_and_single(client.get_collections) 
    _list_and_single(client.get_containers)
    _list_and_single(client.get_distributions)
    _list_and_single(client.get_institutions)
    _list_and_single(client.get_modules)
    _list_and_single(client.get_operations)
    _list_and_single(client.get_orders)
    _list_and_single(client.get_organisms)
    _list_and_single(client.get_parts)
    _list_and_single(client.get_plans)
    _list_and_single(client.get_plates)
    _list_and_single(client.get_platesets)
    _list_and_single(client.get_protocols)
    _list_and_single(client.get_robots)
