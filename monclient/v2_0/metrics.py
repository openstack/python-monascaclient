# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# manages the metrics resource

from monclient.openstack.common.apiclient import base


class Metrics(base.Resource):

    def __repr__(self):
        return "<Metrics %s>" % self._info


class MetricsManager(base.BaseManager):
    resource_class = Metrics
    base_url = '/metrics'

    def getHeaders(self, args):
        headers = self.client.credentials_headers()
        if args.runlocal:
            # add temp header, used when running locally.
            if args.os_tenant_id:
                headers['X-Tenant-Id'] = args.os_tenant_id
            else:
                headers['X-Tenant-Id'] = '1234'
        return headers

    def create(self, args, **kwargs):
        """Create a metric."""
        resp, body = self.client.json_request('POST', self.base_url,
                                              data=kwargs,
                                              headers=self.getHeaders(args))
        return body
