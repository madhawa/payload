# Copyright (C) 2013-2014 PolyBeacon, Inc.
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


class QueueCaller(object):

    def __init__(
            self, uuid, created_at, member_uuid, name, number, position,
            queue_id, status, status_at):
        self.created_at = created_at
        self.member_uuid = member_uuid
        self.name = name
        self.number = number
        self.position = position
        self.queue_id = queue_id
        self.status = status
        self.status_at = status_at
        self.uuid = uuid


class QueueMember(object):

    def __init__(
            self, uuid, created_at, number, paused, paused_at, queue_id,
            status, status_at):
        self.created_at = created_at
        self.number = number
        self.paused = paused
        self.paused_at = paused_at
        self.queue_id = queue_id
        self.status = status
        self.status_at = status_at
        self.uuid = uuid
