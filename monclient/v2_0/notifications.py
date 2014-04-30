'''
Created on Mar 25, 2014

'''
from monclient.common import mon_manager
from monclient.openstack.common.apiclient import base


class Notifications(base.Resource):

    def __repr__(self):
        return "<Notifications %s>" % self._info


class NotificationsManager(mon_manager.MonManager):
    resource_class = Notifications
    base_url = '/notification-methods'

    def create(self, **kwargs):
        """Create a notification."""
        newheaders = self.get_headers()
        resp, body = self.client.json_request('POST', self.base_url,
                                              data=kwargs,
                                              headers=newheaders)
        return body

    def get(self, **kwargs):
        """Get the details for a specific notification."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['notification_id']
        resp, body = self.client.json_request('GET', url_str,
                                              headers=newheaders)
        return body

    def list(self):
        """Get a list of notifications."""
        newheaders = self.get_headers()
        resp, body = self.client.json_request(
            'GET', self.base_url, headers=newheaders)
        return body

    def delete(self, **kwargs):
        """Delete a notification."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['notification_id']
        resp, body = self.client.json_request(
            'DELETE', url_str, headers=newheaders)
        return resp

    def update(self, **kwargs):
        """Update a notification."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['notification_id']
        del kwargs['notification_id']
        resp, body = self.client.json_request(
            'PUT', url_str,
            data=kwargs,
            headers=newheaders)
        return body
