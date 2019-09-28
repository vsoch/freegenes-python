
# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

__version__ = "0.0.13"
AUTHOR = 'Vanessa Sochat'
AUTHOR_EMAIL = 'vsochat@stanford.edu'
NAME = 'freegenes'
PACKAGE_URL = "http://www.github.com/vsoch/freegenes-python"
KEYWORDS = 'FreeGenes node API client'
DESCRIPTION = "Command line python tool for working with FreeGenes."
LICENSE = "LICENSE"

INSTALL_REQUIRES = (
    ('semver', {'min_version': '2.8.0'}),
    ('requests', {'min_version': '2.21.0'}),
)

TESTS_REQUIRES = (
    ('pytest', {'min_version': '4.6.2'}),
)
