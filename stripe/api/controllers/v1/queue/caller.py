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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pecan
import wsme

from pecan import rest
from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from stripe.api.controllers.v1 import base
from stripe.common import exception
from stripe.middleware import models
from stripe.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class QueueCaller(base.APIBase):
    """API representation of a queue caller."""

    id = int
    called_id = wtypes.text
    caller_id = wtypes.text
    caller_name = wtypes.text
    queue_id = int

    def __init__(self, **kwargs):
        self.fields = vars(models.QueueCaller)
        for k in self.fields:
            setattr(self, k, kwargs.get(k))


class QueueCallersController(rest.RestController):
    """REST Controller for queue callers."""

    @wsme_pecan.wsexpose(None, wtypes.text, wtypes.text, status_code=204)
    def delete(self, queue_id, id):
        """Delete a queue caller."""
        pecan.request.middleware_api.delete_queue_caller(
            queue_id=queue_id, id=id
        )

    @wsme_pecan.wsexpose([QueueCaller], unicode)
    def get_all(self, queue_id):
        """Retrieve a list of queue callers."""
        res = pecan.request.middleware_api.list_queue_callers(
            queue_id=queue_id
        )

        return res

    @wsme_pecan.wsexpose(QueueCaller, unicode, unicode)
    def get_one(self, queue_id, id):
        """Retrieve information about the given queue."""
        try:
            result = pecan.request.middleware_api.get_queue_caller(
                queue_id=queue_id, id=id
            )
        except exception.QueueCallerNotFound:
            # TODO(pabelanger): See if there is a better way of handling
            # exceptions.
            raise wsme.exc.ClientSideError('Not found')

        return result
