from monclient import client
import time

# init endpoint - use either keystone to get it, or user input endpoint
# reference monclient.shell.py for how to use keystone.
endpoint = 'http://192.168.10.4:8080/v2.0'

api_version = '2_0'

# init kwargs.  Refer to monclient.shell.py to see possible args when
# using keystone, they differ slightly.
kwargs = {
    'username': '',
    'password': '',
    'token': '12345678',
    'tenant_id': '87247213431361',
    'tenant_name': '',
    'auth_url': '',
    'service_type': '',
    'endpoint_type': '',
    'insecure': False
}

# construct the mon client
mon_client = client.Client(api_version, endpoint, **kwargs)

# reference the monclient.v2_0.shell.py do_
# commands for command fields

# post a metric
dimensions = {'instance_id': '12345', 'service': 'hello'}
fields = {}
fields['name'] = 'cindy1'
fields['dimensions'] = dimensions
fields['timestamp'] = time.time()
fields['value'] = 222.333
resp = mon_client.metrics.create(**fields)
# throws an exception if it fails
print(resp)
print('Successfully created metric')


# metric-list
name = 'cindy1'
dimensions = None
fields = {}
if name:
    fields['name'] = name
if dimensions:
    fields['dimensions'] = dimensions
body = mon_client.metrics.list(**fields)
# throws an exception if it fails
print(body)
