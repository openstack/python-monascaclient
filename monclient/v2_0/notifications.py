'''
Created on Mar 25, 2014

'''
from monclient.openstack.common.apiclient import base


class Notifications(base.Resource):

    def __repr__(self):
        return "<Notifications %s>" % self._info


class NotificationsManager(base.BaseManager):
    resource_class = Notifications

    def create(self, runlocal=False, **kwargs):
        """Create a notification."""
        headers = self.client.credentials_headers()
        if runlocal:
            # temp header, used when running locally.
            headers['X-Tenant-Id'] = '1'
        resp, body = self.client.json_request('POST', '/notification-methods',
                                              data=kwargs, headers=headers)
        return body
