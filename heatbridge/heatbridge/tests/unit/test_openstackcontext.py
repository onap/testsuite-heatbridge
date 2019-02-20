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
from heatbridge.OpenstackContext import OpenstackContext


class openstackContextTestingBase(unittest.TestCase):

    """The super class which testing classes could inherit."""

    logging.disable(logging.CRITICAL)

    def setUp(self):
        username = 'test_username'
        password = 'test_password'
        tenant = 'test_tenant_id'
        region = 'test_region'
        owner = 'test_owner'
        domain_id = 'test_domain_id'
        domain_id = 'test_project_name'
        self.test = OpenstackContext(username, password, tenant,
                                     region, owner, domain_id, domain_id)


if __name__ == "__main__":
    # logging must be disabled else it calls time.time()
    # what will break these unit tests.
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
