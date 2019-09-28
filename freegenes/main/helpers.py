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

def derive_parts(self, sequence):
    '''based on a sequence, search all freegenes parts for the sequence,
       forward and backwards. This is done by the client (and not on the
       server) as to not tax the server. We cache the parts request to
       not make the same one over and over.

       Algorithm:
       =========
       1. Cache all parts from the API (one call)
       2. Find all forward and reverse substrings that match
       3. Model as interview scheduling problem

       If the user is interested in ALL possible combinations of parts,
       we would want to remove the "best solution" parts (the first part)
       from the list and try again.
    '''
    self._cache_parts()

    # Parts found to match
    coords = []

    for uuid, part in self.cache['parts'].items():

        # Only use parts with optimized sequences
        if part.get('optimized_sequence'):
            forward = part['optimized_sequence']
            reverse = forward[::-1]

            # Case 1: we found the forward sequence
            if forward in sequence:
                for match in re.finditer(forward, sequence): 
                    coords.append((part.get('uuid'), ">", match.start(), match.end()))

            # Case 2: we found the reverse sequence
            if reverse in sequence:
                for match in re.finditer(reverse, sequence): 
                    coords.append((part.get('uuid'), "<", match.start(), match.end()))

    # Make a queue sorted by how long they (end - start)
    queue = sorted(coords, key=lambda tup: tup[3]-tup[2])

    def overlaps_with(selected_sequences, element):
        '''determine if an element overlaps with any current elements in the
           list
        '''
        for selected in selected_sequences:

           # If the element start is greater than selected start, less than end
           if (element[2] >= selected[2]) and (element[2] < selected[3]):
               return True

           # If the element end is greater than the selected start, less than end
           if (element[3] > selected[2]) and (element[3] <= selected[3]):
               return True

        return False
 
    selected_sequences = []

    while queue:

        # Pop the longest element ( the last )
        element = queue.pop()

        # If there is no overlap add
        if not overlaps_with(selected_sequences, element):
            selected_sequences.append(element)

    # Need to sort them again, by the start
    selected_sequences = sorted(selected_sequences, key=lambda tup: tup[2])

    return selected_sequences
