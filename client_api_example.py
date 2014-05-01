from monclient import client
import monclient.exc as exc
import time

# In order to use the python api directly, you must first obtain an
# auth token and identify which endpoint you wish to speak to.
endpoint = 'http://192.168.10.4:8080/v2.0'

# The api version of mon-api
api_version = '2_0'

# There are other kwarg options (ca files) used for http request.
# Refer to monclient.shell.py for other kwargs supported.
kwargs = {}
kwargs['token'] = '12345678'

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
try:
    resp = mon_client.metrics.create(**fields)
except exc.HTTPException as he:
    print('HTTPException code=%s message=%s' % (he.code, he.message))
else:
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
try:
    body = mon_client.metrics.list(**fields)
except exc.HTTPException as he:
    print('HTTPException code=%s message=%s' % (he.code, he.message))
else:
    print(body)
