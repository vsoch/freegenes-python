'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from freegenes.version import __version__
from freegenes.logger import bot
import requests
import os

class Client(object):

    def __init__(self, token=None, base="https://freegenes.dev"):
 
        self._set_base(base)
        self._set_token(token)
        self._set_headers()
        self._test_token()

    def __repr__(self):
        return "[client][freegenes][%s]" % __version__

    def __str__(self):
        return "[client][freegenes][%s]" % __version__

    def _set_token(self, token):
        '''ensure that token provided, or FREEGENES_TOKEN is defined in environ
        '''
        self.token = os.environ.get('FREEGENES_TOKEN', token)
        if not self.token:
            bot.exit("You must provide a token or export FREEGENES_TOKEN.")

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
        if requests.head("%s" % self.base, headers=self.headers).status_code != 200:
            bot.exit('Provided token is invalid.')


    # Specific API calls

    def get(self, url, headers=None, page=None, paginate=True):
        '''the default get, will use default headers if custom aren't defined.
           we take a partial url (e.g., /api/authors) and then add the base.

           Parameters
           ==========
           url: the url endpoint to query (without the http/s or domain)
           headers: if defined, don't use default headers.
           page: obtain a specific page of the result.
           paginate: obtain all pages after query (default is True)
        '''
        heads = headers or self.headers
        fullurl = "%s%s" %(self.base, url)

        # If we are provided a page
        if page:
            fullurl = "%s?page=%s" %(fullurl, page)
        response = requests.get(fullurl, headers=heads)

        # Return a successful response
        if response.status_code == 200:
 
            results = response.json()

            # Listings will have results, single entity not
            if "results" in results:
                results = results['results']

            # Are there pages?
            if paginate:
                while response.next:
                    results = results + self.get(url, headers, page=response.next)
            return results

        bot.exit("Error with %s, return value %s: %s" %(url, response.status_code, response.reason))


    # Endpoints

    def get_entity(self, name, uuid=None):
        '''return a single entity if a uuid is provided, otherwise a list

           Parameters
           ==========
           uuid: the unique resource identifier of the entity
        '''
        if uuid:
            return self.get('/api/%s/%s' % (name, uuid))
        return self.get('/api/%s' % name)


    def get_authors(self, uuid=None):
        return self.get_entity('authors', uuid)

    def get_collections(self, uuid=None):
        return self.get_entity('collections', uuid)

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
