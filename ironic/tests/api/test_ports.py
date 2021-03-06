# vim: tabstop=4 shiftwidth=4 softtabstop=4
# -*- encoding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Tests for the API /ports/ methods.
"""

from ironic.openstack.common import uuidutils
from ironic.tests.api import base
from ironic.tests.db import utils as dbutils


class TestListChassis(base.FunctionalTest):

    def test_empty(self):
        data = self.get_json('/ports')
        self.assertEqual([], data)

    def test_one(self):
        ndict = dbutils.get_test_port()
        port = self.dbapi.create_port(ndict)
        data = self.get_json('/ports')
        self.assertEqual(port['uuid'], data[0]["uuid"])

    def test_many(self):
        ch_list = []
        for id in xrange(5):
            ndict = dbutils.get_test_port(id=id,
                                          uuid=uuidutils.generate_uuid())
            ports = self.dbapi.create_port(ndict)
            ch_list.append(ports['uuid'])
        data = self.get_json('/ports')
        self.assertEqual(len(ch_list), len(data))

        uuids = [n['uuid'] for n in data]
        self.assertEqual(ch_list.sort(), uuids.sort())

    def test_links(self):
        uuid = uuidutils.generate_uuid()
        ndict = dbutils.get_test_port(id=1, uuid=uuid)
        self.dbapi.create_port(ndict)
        data = self.get_json('/ports/1')
        self.assertIn('links', data.keys())
        self.assertEqual(len(data['links']), 2)
        self.assertIn(uuid, data['links'][0]['href'])
