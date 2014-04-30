'''
Created on Apr 29, 2014

'''

from monclient.openstack.common.apiclient import base


class MonManager(base.BaseManager):

    def __init__(self, client, **kwargs):
        super(MonManager, self).__init__(client)

    def get_headers(self):
        headers = self.client.credentials_headers()
        return headers
