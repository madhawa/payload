# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013 PolyBeacon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from payload.common import exception
from payload.tests.db import base


class TestCase(base.FunctionalTest):

    def setUp(self):
        super(TestCase, self).setUp()
        self.queue = self._create_test_queue()
        self.agent = self._create_test_agent()

    def test_create_queue_member(self):
        res = self._create_test_queue_member(
            agent_uuid=self.agent['uuid'], queue_uuid=self.queue['uuid'])
        self.assertTrue(res)

    def test_delete_queue_member(self):
        self._create_test_queue_member(
            agent_uuid=self.agent['uuid'], queue_uuid=self.queue['uuid'])
        self.db_api.delete_queue_member(
            agent_uuid=self.agent['uuid'], queue_uuid=self.queue['uuid'])
        self.assertRaises(
            exception.QueueMemberNotFound, self.db_api.get_queue_member,
            self.agent['uuid'], self.queue['uuid'])

    def test_delete_queue_member_not_found(self):
        self.assertRaises(
            exception.QueueMemberNotFound, self.db_api.delete_queue_member,
            123, 123)

    def test_get_queue_member(self):
        member = self._create_test_queue_member(
            agent_uuid=self.agent['uuid'], queue_uuid=self.queue['uuid'])
        res = self.db_api.get_queue_member(
            agent_uuid=self.agent['uuid'], queue_uuid=self.queue['uuid'])
        self.assertEqual(member['agent_uuid'], res['agent_uuid'])

    def test_list_queue_members(self):
        self._create_test_queue_member(
            agent_uuid=self.agent['uuid'], queue_uuid=self.queue['uuid'])
        res = self.db_api.list_queue_members(self.queue['uuid'])
        self.assertTrue(res)
