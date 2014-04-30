'''
Created on Mar 31, 2014

'''
from monclient.common import mon_manager
from monclient.openstack.common.apiclient import base


class Alarms(base.Resource):

    def __repr__(self):
        return "<Alarms %s>" % self._info


class AlarmsManager(mon_manager.MonManager):
    resource_class = Alarms
    base_url = '/alarms'

    def create(self, **kwargs):
        """Create an alarm."""
        newheaders = self.get_headers()
        resp, body = self.client.json_request('POST', self.base_url,
                                              data=kwargs,
                                              headers=newheaders)
        return body

    def get(self, **kwargs):
        """Get the details for a specific alarm."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        resp, body = self.client.json_request('GET', url_str,
                                              headers=newheaders)
        return body

    def list(self):
        """Get a list of alarms."""
        newheaders = self.get_headers()
        resp, body = self.client.json_request(
            'GET', self.base_url, headers=newheaders)
        return body

    def delete(self, **kwargs):
        """Delete a specific alarm."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        resp, body = self.client.json_request('DELETE', url_str,
                                              headers=newheaders)
        return resp

    def update(self, **kwargs):
        """Update a specific alarm."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        del kwargs['alarm_id']
        resp, body = self.client.json_request('PUT', url_str,
                                              data=kwargs,
                                              headers=newheaders)
        return body

    def patch(self, **kwargs):
        """Patch a specific alarm."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s' % kwargs['alarm_id']
        del kwargs['alarm_id']
        resp, body = self.client.json_request('PATCH', url_str,
                                              data=kwargs,
                                              headers=newheaders)
        return body

    def history(self, **kwargs):
        """History of a specific alarm."""
        newheaders = self.get_headers()
        url_str = self.base_url + '/%s/state-history' % kwargs['alarm_id']
        del kwargs['alarm_id']
        resp, body = self.client.json_request('GET', url_str,
                                              headers=newheaders)
        return body
