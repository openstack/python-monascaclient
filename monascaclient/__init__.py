# Copyright 2017 FUJITSU LIMITED
#
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

"""

Patches method that transforms error responses.
That is required to handle different format monasca follows.

"""

from keystoneauth1 import exceptions as exc
from keystoneauth1.exceptions import http


def mon_exc_from_response(response, method, url):
    req_id = response.headers.get('x-openstack-request-id')

    kwargs = {
        'http_status': response.status_code,
        'response': response,
        'method': method,
        'url': url,
        'request_id': req_id,
    }
    if 'retry-after' in response.headers:
        kwargs['retry_after'] = response.headers['retry-after']

    content_type = response.headers.get('Content-Type', '')
    if content_type.startswith('application/json'):
        try:
            body = response.json()
        except ValueError:
            pass
        else:
            if isinstance(body, dict):
                if isinstance(body.get('error'), dict):
                    error = body['error']
                    kwargs['message'] = error.get('message')
                    kwargs['details'] = error.get('details')
                elif {'description', 'title'} <= set(body):
                    # monasca-api error response structure
                    kwargs['message'] = body.get('title')
                    kwargs['details'] = body.get('description')
    elif content_type.startswith('text/'):
        kwargs['details'] = response.text

    try:
        cls = http._code_map[response.status_code]
    except KeyError:
        if 500 <= response.status_code < 600:
            cls = exc.HttpServerError
        elif 400 <= response.status_code < 500:
            cls = exc.HTTPClientError
        else:
            cls = exc.HttpError
    return cls(**kwargs)


exc.from_response = mon_exc_from_response
