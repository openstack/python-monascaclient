'''
Created on Mar 25, 2014

'''
from monclient.openstack.common.apiclient import base


class Notifications(base.Resource):

    def __repr__(self):
        return "<Notifications %s>" % self._info


class NotificationsManager(base.BaseManager):
    resource_class = Notifications
    base_url = '/notification-methods'

    def get_headers(self, args):
        headers = self.client.credentials_headers()
        if args.runlocal:
            # add temp header, used when running locally.
            if args.os_tenant_id:
                headers['X-Tenant-Id'] = args.os_tenant_id
            else:
                headers['X-Tenant-Id'] = '1234'
        return headers

    def create(self, args, **kwargs):
        """Create a notification."""
        resp, body = self.client.json_request('POST', self.base_url,
                                              data=kwargs,
                                              headers=self.get_headers(args))
        return body

    def get(self, args, **kwargs):
        """Get the details for a specific notification."""
        url_str = self.base_url + '/%s' % kwargs['notification_id']
        resp, body = self.client.json_request('GET', url_str,
                                              headers=self.get_headers(args))
        return body

    def list(self, args):
        """Get a list of notifications."""
        resp, body = self.client.json_request(
            'GET', self.base_url, headers=self.get_headers(args))
        return body
