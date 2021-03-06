# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
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

"""Tests for manipulating Chassis via the DB API"""

from ironic.common import exception
from ironic.db import api as dbapi
from ironic.openstack.common import uuidutils
from ironic.tests.db import base
from ironic.tests.db import utils


class DbChassisTestCase(base.DbTestCase):

    def setUp(self):
        super(DbChassisTestCase, self).setUp()
        self.dbapi = dbapi.get_instance()

    def _create_test_chassis(self, **kwargs):
        ch = utils.get_test_chassis(**kwargs)
        self.dbapi.create_chassis(ch)
        return ch

    def test_get_chassis_list(self):
        uuids = []
        for i in xrange(1, 6):
            n = utils.get_test_chassis(id=i, uuid=uuidutils.generate_uuid())
            self.dbapi.create_chassis(n)
            uuids.append(unicode(n['uuid']))
        res = self.dbapi.get_chassis_list()
        uuids.sort()
        res.sort()
        self.assertEqual(uuids, res)

    def test_get_chassis_by_id(self):
        ch = self._create_test_chassis()
        chassis = self.dbapi.get_chassis(ch['id'])

        self.assertEqual(chassis['uuid'], ch['uuid'])

    def test_get_chassis_by_uuid(self):
        ch = self._create_test_chassis()
        chassis = self.dbapi.get_chassis(ch['uuid'])

        self.assertEqual(chassis['id'], ch['id'])

    def test_get_chassis_that_does_not_exist(self):
        self.assertRaises(exception.ChassisNotFound,
                          self.dbapi.get_chassis, 666)

    def test_update_chassis(self):
        ch = self._create_test_chassis()
        new_uuid = uuidutils.generate_uuid()

        ch['uuid'] = new_uuid
        res = self.dbapi.update_chassis(ch['id'], {'uuid': new_uuid})

        self.assertEqual(res['uuid'], new_uuid)

    def test_update_chassis_that_does_not_exist(self):
        new_uuid = uuidutils.generate_uuid()

        self.assertRaises(exception.ChassisNotFound,
                          self.dbapi.update_chassis, 666, {'uuid': new_uuid})

    def test_destroy_chassis(self):
        ch = self._create_test_chassis()
        self.dbapi.destroy_chassis(ch['id'])

        self.assertRaises(exception.ChassisNotFound,
                          self.dbapi.get_chassis, ch['id'])

    def test_destroy_chassis_that_does_not_exist(self):
        self.assertRaises(exception.ChassisNotFound,
                          self.dbapi.destroy_chassis, 666)
