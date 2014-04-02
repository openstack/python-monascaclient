'''
Created on Mar 31, 2014

'''
from monclient.openstack.common.apiclient import base


class Alarms(base.Resource):

    def __repr__(self):
        return "<Alarms %s>" % self._info


class AlarmsManager(base.BaseManager):
    resource_class = Alarms
    base_url = '/alarms'

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
        """Create an alarm."""
        resp, body = self.client.json_request('POST', self.base_url,
                                              data=kwargs,
                                              headers=self.getHeaders(args))
        return body

    def get(self, args, **kwargs):
        """Get the details for a specific alarm."""
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        resp, body = self.client.json_request('GET', url_str,
                                              headers=self.getHeaders(args))
        return body

    def list(self, args):
        """Get a list of alarms."""
        resp, body = self.client.json_request(
            'GET', self.base_url, headers=self.getHeaders(args))
        return body
