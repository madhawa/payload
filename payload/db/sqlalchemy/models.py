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

import json

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import schema
from sqlalchemy import String
from sqlalchemy.types import TypeDecorator
from sqlalchemy.types import VARCHAR

from payload.openstack.common.db.sqlalchemy import models


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string."""

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class PayloadBase(models.TimestampMixin, models.ModelBase):

    metadata = None


Base = declarative_base(cls=PayloadBase)


class Agent(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(255))
    user_id = Column(String(255))
    uuid = Column(String(255), unique=True)


class Queue(Base):
    __tablename__ = 'queues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(JSONEncodedDict)
    disabled = Column(Boolean, default=False)
    name = Column(String(80))
    project_id = Column(String(255))
    user_id = Column(String(255))
    uuid = Column(String(255), unique=True)


class QueueMember(Base):
    __tablename__ = 'queue_members'
    __table_args__ = (
        schema.UniqueConstraint(
            'agent_uuid', 'queue_uuid',
            name='uniq_queue_members0agent_uuid0queue_uuid'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_uuid = Column(String(255), ForeignKey('agents.uuid'))
    queue_uuid = Column(String(255), ForeignKey('queues.uuid'))
