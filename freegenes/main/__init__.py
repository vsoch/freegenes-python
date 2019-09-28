'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from freegenes.version import __version__
from freegenes.logger import bot

from .helpers import derive_parts
from .cache import cache_parts

import requests
import os
import re

class Client(object):

    def __init__(self, token=None, base="https://freegenes.dev", validate=True):
 
        self.validate = validate
        self._set_base(base)
        self._set_token(token)
        self._set_headers()
        self._test_token()
        self.cache = {}

    def __repr__(self):
        return "[client][freegenes][%s]" % __version__

    def __str__(self):
        return "[client][freegenes][%s]" % __version__

    def _set_token(self, token):
        '''ensure that token provided, or FREEGENES_TOKEN is defined in environ
        '''
        self.token = os.environ.get('FREEGENES_TOKEN', token)
        if not self.token:
            if self.validate:
                bot.exit("You must provide a token or export FREEGENES_TOKEN.")
            bot.warning("No token provided, API will not function as expected.")

    def _set_base(self, base):
        '''look for FREEGENES_BASE defined in environ
        '''
        self.base = os.environ.get('FREEGENES_BASE', base)
        if self.base:
            self.base = self.base.strip('/')

    def _set_headers(self):
        '''set the headers to the default, meaning we provide an
           authorization token.
        '''
        self.headers = {
          "Accept": "application/json",
          "Authorization": "Token %s" % self.token
        }

    def _test_token(self):
        '''test that the token works - this function also ensures
           that the base is correct.
        '''
        if self.validate:
            if requests.head("%s" % self.base, headers=self.headers).status_code != 200:
                bot.exit('Provided token is invalid.')

    # Specific API calls

    def get(self, url, headers=None, paginate=True, limit=1000):
        '''the default get, will use default headers if custom aren't defined.
           we take a partial url (e.g., /api/authors) and then add the base.

           Parameters
           ==========
           url: the url endpoint to query (without the http/s or domain)
           headers: if defined, don't use default headers.
           paginate: obtain all pages after query (default is True)
           limit: number of responses per query (default 1000)
        '''
        heads = headers or self.headers

        # A second call will already provide a complete url
        fullurl = "%s%s?limit=%s" %(self.base, url, limit)
        if url.startswith('http'):
            fullurl = url

        response = requests.get(fullurl, headers=heads)

        # Return a successful response
        if response.status_code == 200:
 
            response = response.json()
            results = response

            # Listings will have results, single entity not
            if "results" in response:
                results = response['results']

            # Are there pages (but the user doesn't want a specific one)
            if paginate:
                next_url = response.get('next')
                if next_url is not None:
                    return results + self.get(next_url, headers)
            return results

        bot.error("Error with %s, return value %s: %s" %(url, response.status_code, response.reason))
        return response

    def post(self, url, data=None, headers=None):
        '''the default post, will use default headers if custom aren't defined.
           we take a partial url (e.g., /api/authors) and then add the base.

           Parameters
           ==========
           url: the url endpoint to query (without the http/s or domain)
           data: data to add to the request.
           headers: if defined, don't use default headers.
        '''
        heads = headers or self.headers
        fullurl = "%s%s" %(self.base, url)

        # Remove empty / None fields from data
        if data:
            data = {k:v for k,v in data.items() if v}

        print(data)
        response = requests.post(fullurl, headers=heads, data=data)

        # Return a successful response
        if response.status_code in [200, 201]: 
            return response.json()

        bot.error("Error with %s, return value %s: %s" %(url, response.status_code, response.reason))
        return response


    def create_entity(self, name, data=None):
        '''create an entity with a POST request.

           Parameters
           ==========
           name: the name of the endpoint to post to.
           data: key word arguments to include.
        '''
        return self.post('/api/%s/' % name, data=data)


    # GET Endpoints

    def get_entity(self, name, uuid=None):
        '''return a single entity if a uuid is provided, otherwise a list

           Parameters
           ==========
           uuid: the unique resource identifier of the entity
        '''
        if uuid:
            return self.get('/api/%s/%s/' % (name, uuid))
        return self.get('/api/%s/' % name)


    def get_authors(self, uuid=None):
        return self.get_entity('authors', uuid)

    def get_collections(self, uuid=None):
        return self.get_entity('collections', uuid)

    def get_compositeparts(self, uuid=None):
        return self.get_entity('compositeparts', uuid)

    def get_containers(self, uuid=None):
        return self.get_entity('containers', uuid)

    def get_distributions(self, uuid=None):
        return self.get_entity('distributions', uuid)

    def get_institutions(self, uuid=None):
        return self.get_entity('institutions', uuid)

    def get_modules(self, uuid=None):
        return self.get_entity('modules', uuid)

    def get_operations(self, uuid=None):
        return self.get_entity('operations', uuid)

    def get_orders(self, uuid=None):
        return self.get_entity('orders', uuid)

    def get_organisms(self, uuid=None):
        return self.get_entity('organisms', uuid)

    def get_parts(self, uuid=None):
        return self.get_entity('parts', uuid)

    def get_plans(self, uuid=None):
        return self.get_entity('plans', uuid)

    def get_plates(self, uuid=None):
        return self.get_entity('plates', uuid)

    def get_platesets(self, uuid=None):
        return self.get_entity('platesets', uuid)

    def get_protocols(self, uuid=None):
        return self.get_entity('protocols', uuid)

    def get_robots(self, uuid=None):
        return self.get_entity('robots', uuid)

    # POST Endpoints (create)

    def create_composite_part(self, name, 
                                    sequence,
                                    part_ids=None,
                                    description=None,
                                    direction_string=None,
                                    composite_id=None,
                                    composite_type=None):
        '''create a new composite part from a sequence. If no parts are provided,
           then we search the provided sequence for all parts in FreeGenes, and
           make the association (and derive directions). The data for the parts
           is cached with the client so we only need to derive it once.
           
           Parameters
           ==========
           name: a name for the composite part (required)
           sequence: the new sequence (required)
           part_ids: a list of one or more part ids (optional)
           description: a string description (optional)
           composite_id: a composite id (optional) (like gene_id for a part)
           composite_type: the type of composite part (optional)
        '''
        # If part ids not defined, we need to search sequence
        if not part_ids:

            # [(uuid, direction, start, end),
            selected_parts = self._derive_parts(sequence)
            part_ids = [x[0] for x in selected_parts]
            direction_string = "".join([x[1] for x in selected_parts])

        data = {"name": name,
                "parts": part_ids,
                "sequence": sequence,
                "description": description,
                "direction_string": direction_string,
                "composite_id": composite_id,
                "composite_type": composite_type}
       
        return self.create_entity("compositeparts", data)



# Helper and Caching Functions

Client._derive_parts = derive_parts
Client._cache_parts = cache_parts
