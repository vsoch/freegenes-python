'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from freegenes.version import __version__
from freegenes.utils import str2csv
from freegenes.logger import bot
import requests
import os

class Client(object):

    def __init__(self, email=None, token=None, eutoken=None, 
                       base="https://twist-api.twistbioscience-staging.com/", version="v1"):
        '''Generate a client for interacting with Twist.  I was unable to generate
           tokens using the API (it doesn't work), and the head of Twist (Gil Raytan) 
           had to manually send them.

           Endpoints:
             production: https://twist-api.twistdna.com
             staging: https://twist-api.twistbioscience-staging.com/

           Parameters
           ==========
           token: the general api token
           eutoken: the end user token
        '''
        self.version = version
        self._set_base(base)
        self._set_tokens(token, eutoken)
        self._set_headers()
        self._test_token()
        self._set_email(email)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[client][twist]"

    def _set_tokens(self, token, eutoken):
        '''ensure that token provided, or look for FREEGENES_TWIST_TOKEN 
           or FREEGENES_TWIST_LOGIN and FREEGENES_TWIST_PASSWORD defined in 
           in the environment.
        '''
        self.token = os.environ.get('FREEGENES_TWIST_TOKEN', token)
        self.eutoken = os.environ.get('FREEGENES_TWIST_EUTOKEN', eutoken)

        if not self.token or not self.eutoken:

            username = os.environ.get('FREEGENES_TWIST_LOGIN')
            password = os.environ.get('FREEGENES_TWIST_PASSWORD')

            # username and password are required to get a token
            if not username or not password:
                bot.exit("You must export FREEGENES_TWIST_TOKEN or FREEGENES_TWIST_LOGIN and FREEGENES_TWIST_PASSWORD")

            headers = {"username": username, "password": password}
            response = requests.post(self.base + '/api-token-auth/', headers=headers)
            if response.status_code != 201:
                bot.exit("Error with authentication, %s:%s" %(response.reason, response.status_code))
            self.token = response.json()['token']


    def _set_base(self, base):
        '''look for FREEGENES_TWIST_BASE defined in environ
        '''
        self.base = os.environ.get('FREEGENES_TWIST_BASE', base)
        if self.base:
            self.base = self.base.strip('/')


    def _get_email(self, email):
        '''get an email (required) either provided by calling function or
           already set in client. Exit if not defined.

           Parameters
           ==========
           email: the email address associated with Twist
        '''
        email = email or self.email
        if not email:
            bot.exit("Email must provided to client, calling function, or in environment FREEGENES_TWIST_EMAIL.")
        return email


    def _set_email(self, email):
        '''look for FREEGENES_TWIST_EMAIL defined in environ
        '''
        self.email = os.environ.get('FREEGENES_TWIST_EMAIL', email)
        if not email:
            self.whoami()
        

    def _set_headers(self):
        '''set the headers to the default, meaning we provide an
           authorization token.
        '''
        self.headers = {
          "Accept": "application/json",
          "Accept-Encoding": "json",
          "Authorization": "JWT %s" % self.token,
          "X-End-User-Token": self.eutoken         
        }

    def _test_token(self):
        '''test that the token works - this function also ensures
           that the base is correct.
        '''
        if requests.head("%s" % self.base, headers=self.headers).status_code not in [200, 302]:
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

    def whoami(self):
        '''Returns the authentication APIClient username. 
           And email when EUT is supplied.
        '''
        result = self.get('/whoami/')
   
        # If the client did not provide an email, try getting it
        if not self.email and "email" in result:
            self.email = result["email"]
        return result


    def healthcheck(self):
        '''Returns the API healthcheck endpoint --> {'status': 'OK'}
        '''
        return self.get('/healthcheck/')


    def is_alive(self):
        '''Returns if the API is alive --> {'status': 'OK'}
        '''
        return self.get('/is_alive/')


    def version(self):
        '''Returns the API version information, including a dictionary with
           version, tag, branch, and git_commit.
        '''
        return self.get('/version/')


    # Accounts

    def accounts(self):
        '''Return accounts associated
        '''
        return self.get('/v1/accounts/')


    def account(self, account_id):
        '''Look up a specific account based on account id.
        '''
        return self.get('/v1/accounts/%s' % account_id)


    def account_contacts(self, account_id):
        '''Look up account contacts based on account id.
        '''
        return self.get('/v1/accounts/%s/contacts' % account_id)


    def account_users(self, account_id):
        '''Look up account users based on account id.
        '''
        return self.get('/v1/accounts/%s/users' % account_id)


    def account_prices(self, account_id):
        '''Look up account prices based on account id.
        '''
        return self.get('/v1/accounts/%s/prices' % account_id)


    # Catalog Items

    def catalog_items(self):
        '''Look up account prices based on account id.
        '''
        return self.get('/v1/catalog-items')


    def user(self, email=None):
        '''Look up user by email.
        '''
        email = self._get_email(email)
        return self.get('/v1/users/%s/' % email)


    def user_addresses(self, email=None):
        '''Look up user by email.
        '''
        email = self._get_email(email)
        return self.get('/v1/users/%s/addresses/' % email)


    def orders(self, email=None):
        '''Look up orders for a user based on email.
        '''
        email = self._get_email(email)
        return self.get('/v1/users/%s/orders/' % email)


    # Orders

    def order_items(self, sfdc_id, email=None):
        '''Look up order items for a user based on email 
           and the order sfdc_id.
        '''
        email = self._get_email(email)
        return self.get('/v1/users/%s/orders/%s/items' % (email, sfdc_id))

    def order_platemaps_by_barcode(self, sfdc_id, barcode, email=None, return_download=False):
        '''Look up order plate maps for a user based on email.
           sfdc_id and barcode.

           Parameters
           ==========
           sfdc_id: should be the order id.
           barcode: the barcode for the shipment
           email: an email to override the default
           return_download: if True, return the entire response with path to download
        '''
        email = self._get_email(email)
        result = self.get('/v1/users/%s/orders/%s/plate-maps/%s' % (email, sfdc_id, barcode))

        # The result returns an amazon file path
        if "platemaps_file_url" in result and not return_download:
            result = requests.get(result["platemaps_file_url"])
            if result.status_code == 200:

                # Return list of rows, first is header row
                result = str2csv(result.text)
        return result


    def order_platemaps(self, sfdc_id, email=None):
        '''A wrapper for order_platemaps_by_barcode, will handle parsing over
           all shipment barcodes from containers for a single order. The
           entire function is a bit slow with the staging API.

           Parameters
           ==========
           sfdc_id: should be the order id.
           email: an email to override the default
        '''
        email = self._get_email(email)
        items = self.order_items(sfdc_id)
        rows = []

        for shipment in items["shipments"]: # typically < 5
            for container in shipment['containers']:
                new_rows = self.order_platemaps_by_barcode(
                               sfdc_id=sfdc_id, 
                               barcode=container["barcode"])
                if not rows:
                    rows = new_rows
                else:
                    rows = rows + new_rows[1:]
        return rows                 


    def order_platemaps_by_shipment(self, sfdc_id, shipment_id, email=None):
        '''Look up order plate maps for a user based on email.
           sfdc_id and shipment id.

           Parameters
           ==========
           sfdc_id: should be the order id.
           shipment_id: should be the shipment id
           email: an email to override the default
        '''
        email = self._get_email(email)
        return self.get('/v1/users/%s/orders/%s/shipments/%s/plate-maps' % (email, sfdc_id, shipment_id))


