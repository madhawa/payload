# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013 PolyBeacon, Inc.
#
# Author: Paul Belanger <paul.belanger@polybeacon.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.

from stripe.db import api as db_api
from stripe.tests.api.v1 import base
from stripe.tests.db import utils


class TestQueueMembersEmpty(base.FunctionalTest):

    def test_empty_get_all(self):
        res = self.get_json('/queues/1/members')
        self.assertEqual(res, [])

    def test_empty_get_one(self):
        res = self.get_json(
            '/queues/1/members/1', expect_errors=True
        )
        self.assertEqual(res.status_int, 500)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(res.json['error_message'])


class TestCase(base.FunctionalTest):

    def setUp(self):
        super(TestCase, self).setUp()
        self.db_api = db_api.get_instance()
        for i in xrange(1, 6):
            self._create_test_queue_member(id=i)

    def _create_test_queue_member(self, **kwargs):
        member = utils.get_test_member(**kwargs)
        new_member = self.db_api.create_member(member)
        queue = utils.get_test_queue(**kwargs)
        new_queue = self.db_api.create_queue(queue)
        queue_member = utils.get_test_queue_member(
            id=kwargs.get('id'), member_id=new_member['id'],
            queue_id=new_queue['id'],
        )
        new_queue_member = self.db_api.create_queue_member(queue_member)
        return new_queue_member

    def test_list_queue_members(self):
        res = self.get_json('/queues/1/members')
        res.sort()
        self.assertEquals(5, len(res))
        self.assertEquals([1, 2, 3, 4, 5], res)

    def test_delete_queue_member(self):
        self.delete(
            '/queues/1/members/1', status=200
        )
        res = self.get_json('/queues/1/members')
        res.sort()
        self.assertEquals(4, len(res))
        self.assertEquals([2, 3, 4, 5], res)

    def test_get_queue_member(self):
        queue_member = self._create_test_queue_member()
        res = self.get_json('/queues/1/members/%s' % queue_member['id'])
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        self._assertEqualObjects(queue_member, res, ignored_keys)

    def test_create_queue_member(self):
        json = {
            'member_id': 1,
        }
        res = self.post_json(
            '/queues/1/members', params=json, status=200
        )
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'application/json')

    def test_edit_queue_member(self):
        json = {
            'disabled': True,
        }
        res = self.get_json('/queues/1/members')
        self.assertEquals(len(res), 5)
        queue_member_id = res[0]
        self.put_json(
            '/queues/1/members/%s' % queue_member_id, params=json
        )
        queue_member = self.db_api.get_queue_member(queue_member_id)
        self.assertEquals(queue_member.disabled, json['disabled'])