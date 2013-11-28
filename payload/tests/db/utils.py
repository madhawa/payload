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


def get_db_agent(**kw):
    json = {
        'agent_id': kw.get('agent_id', 123),
        'project_id': kw.get('project_id', 'project1'),
    }

    return json


def get_db_queue(**kw):
    queue = {
        'description': 'Example queue',
        'disabled': kw.get('disabled', False),
        'project_id': kw.get('project_id', 'project1'),
        'name': 'example',
    }
    return queue


def get_db_queue_member(**kw):
    queue_member = {
        'queue_uuid': kw.get('queue_uuid', 123),
        'agent_uuid': kw.get('agent_uuid', 123),
    }
    return queue_member
