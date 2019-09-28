'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from freegenes.logger import bot

import requests
import os
import re

def cache_parts(self):
    '''cache the parts for the client
    '''
    if "parts" not in self.cache:
        bot.info("Caching parts for future requests...")
        parts_listing = self.get_parts()
        parts = {}
        for part in parts_listing:
            parts[part['uuid']] = self.get_parts(uuid=part['uuid'])
        self.cache['parts'] = parts
