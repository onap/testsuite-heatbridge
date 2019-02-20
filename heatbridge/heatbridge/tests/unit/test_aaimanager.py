#!/usr/bin/env python

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

# import heatbridge.AAIManager as aaimanager
from heatbridge.AAIManager import AAIManager

__author__ = "Morgan Richomme <morgan.richomme@orange.com>"


class AaiManagerTestingBase(unittest.TestCase):

    """The super class which testing classes could inherit."""

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.context = "a context"

    def test_get_link_found(self):
        links = [{'name': 'link1', 'rel': 'found1', 'href': 'href1'},
                 {'name': 'link2', 'rel': 'found2', 'href': 'href2'}]
        test = AAIManager(self.context)
        self.assertEqual('href1', test.get_link(links, 'found1'))
        self.assertEqual('href2', test.get_link(links, 'found2'))


if __name__ == "__main__":
    # logging must be disabled else it calls time.time()
    # what will break these unit tests.
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
