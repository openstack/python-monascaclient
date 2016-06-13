# (C) Copyright 2014-2016 Hewlett Packard Enterprise Development Company LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import logging
import os
import socket

import requests
import six

from monascaclient import exc
from monascaclient import ksclient
from monascaclient.openstack.common.py3kcompat import urlutils

from oslo_serialization import jsonutils
from oslo_utils import encodeutils

LOG = logging.getLogger(__name__)
if not LOG.handlers:
    LOG.addHandler(logging.StreamHandler())
USER_AGENT = 'python-monascaclient'
CHUNKSIZE = 1024 * 64  # 64kB


def get_system_ca_file():
    """Return path to system default CA file."""
    # Standard CA file locations for Debian/Ubuntu, RedHat/Fedora,
    # Suse, FreeBSD/OpenBSD, MacOSX, and the bundled ca
    ca_path = ['/etc/ssl/certs/ca-certificates.crt',
               '/etc/pki/tls/certs/ca-bundle.crt',
               '/etc/ssl/ca-bundle.pem',
               '/etc/ssl/cert.pem',
               '/System/Library/OpenSSL/certs/cacert.pem',
               requests.certs.where()]
    for ca in ca_path:
        LOG.debug("Looking for ca file %s", ca)
        if os.path.exists(ca):
            LOG.debug("Using ca file %s", ca)
            return ca
    LOG.warn("System ca file could not be found.")


class HTTPClient(object):

    def __init__(self, endpoint, write_timeout=None, read_timeout=None, **kwargs):
        if endpoint.endswith('/'):
            endpoint = endpoint[:-1]
        self.endpoint = endpoint
        self.write_timeout = write_timeout
        self.read_timeout = read_timeout
        self.auth_url = kwargs.get('auth_url')
        self.auth_token = kwargs.get('token')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.user_domain_id = kwargs.get('user_domain_id')
        self.user_domain_name = kwargs.get('user_domain_name')
        self.region_name = kwargs.get('region_name')
        self.include_pass = kwargs.get('include_pass')
        self.endpoint_url = endpoint
        # adding for re-authenticate
        self.project_name = kwargs.get('project_name')
        self.region_name = kwargs.get('region_name')
        self.project_id = kwargs.get('project_id')
        self.domain_id = kwargs.get('domain_id')
        self.domain_name = kwargs.get('domain_name')
        self.endpoint_type = kwargs.get('endpoint_type')
        self.service_type = kwargs.get('service_type')
        self.keystone_timeout = kwargs.get('keystone_timeout')

        self.cert_file = kwargs.get('cert_file')
        self.key_file = kwargs.get('key_file')

        self.ssl_connection_params = {
            'os_cacert': kwargs.get('os_cacert'),
            'cert_file': kwargs.get('cert_file'),
            'key_file': kwargs.get('key_file'),
            'insecure': kwargs.get('insecure'),
        }

        self.verify_cert = None
        if urlutils.urlparse(endpoint).scheme == "https":
            if kwargs.get('insecure'):
                self.verify_cert = False
            else:
                self.verify_cert = kwargs.get(
                    'os_cacert', get_system_ca_file())

    def replace_token(self, token):
        self.auth_token = token

    def re_authenticate(self):
        ks_args = {
            'username': self.username,
            'password': self.password,
            'user_domain_id': self.user_domain_id,
            'user_domain_name': self.user_domain_name,
            'token': '',
            'auth_url': self.auth_url,
            'service_type': self.service_type,
            'endpoint_type': self.endpoint_type,
            'os_cacert': self.ssl_connection_params['os_cacert'],
            'project_id': self.project_id,
            'project_name': self.project_name,
            'domain_id': self.domain_id,
            'domain_name': self.domain_name,
            'insecure': self.ssl_connection_params['insecure'],
            'region_name': self.region_name,
            'keystone_timeout': self.keystone_timeout
        }
        try:
            _ksclient = ksclient.KSClient(**ks_args)
            self.auth_token = _ksclient.token
        except Exception as e:
            raise exc.KeystoneException(e)

    def log_curl_request(self, method, url, kwargs):
        curl = ['curl -i -X %s' % method]

        for (key, value) in kwargs['headers'].items():
            if key in ('X-Auth-Token', 'X-Auth-Key'):
                value = '*****'
            header = '-H \'%s: %s\'' % (encodeutils.safe_decode(key),
                                        encodeutils.safe_decode(value))
            curl.append(header)

        conn_params_fmt = [
            ('key_file', '--key %s'),
            ('cert_file', '--cert %s'),
            ('os_cacert', '--cacert %s'),
        ]
        for (key, fmt) in conn_params_fmt:
            value = self.ssl_connection_params.get(key)
            if value:
                curl.append(fmt % value)

        if self.ssl_connection_params.get('insecure'):
            curl.append('-k')

        if 'data' in kwargs:
            curl.append('-d \'%s\'' % kwargs['data'])

        curl.append('%s%s' % (self.endpoint, url))
        LOG.debug(' '.join(curl))

    @staticmethod
    def log_http_response(resp):
        status = (resp.raw.version / 10.0, resp.status_code, resp.reason)
        dump = ['\nHTTP/%.1f %s %s' % status]
        dump.extend(['%s: %s' % (k, v) for k, v in resp.headers.items()])
        dump.append('')
        if resp.content:
            content = resp.content
            if isinstance(content, six.binary_type):
                content = content.decode('utf-8', 'strict')
            dump.extend([content, ''])
        LOG.debug('\n'.join(dump))

    def _http_request(self, url, method, **kwargs):
        """Send an http request with the specified characteristics.

        Wrapper around requests.request to handle tasks such as
        setting headers and error handling.
        """
        # Copy the kwargs so we can reuse the original in case of redirects
        kwargs['headers'] = copy.deepcopy(kwargs.get('headers', {}))
        kwargs['headers'].setdefault('User-Agent', USER_AGENT)
        if self.auth_token:
            kwargs['headers'].setdefault('X-Auth-Token', self.auth_token)
        else:
            kwargs['headers'].update(self.credentials_headers())
        if self.auth_url:
            kwargs['headers'].setdefault('X-Auth-Url', self.auth_url)
        if self.region_name:
            kwargs['headers'].setdefault('X-Region-Name', self.region_name)
        if self.include_pass and 'X-Auth-Key' not in kwargs['headers']:
            kwargs['headers'].update(self.credentials_headers())

        self.log_curl_request(method, url, kwargs)

        if self.cert_file and self.key_file:
            kwargs['cert'] = (self.cert_file, self.key_file)

        if self.verify_cert is not None:
            kwargs['verify'] = self.verify_cert

        # Since requests does not follow the RFC when doing redirection to sent
        # back the same method on a redirect we are simply bypassing it.  For
        # example if we do a DELETE/POST/PUT on a URL and we get a 302 RFC says
        # that we should follow that URL with the same method as before,
        # requests doesn't follow that and send a GET instead for the method.
        # Hopefully this could be fixed as they say in a comment in a future
        # point version i.e: 3.x
        # See issue: https://github.com/kennethreitz/requests/issues/1704
        allow_redirects = False
        timeout = None
        if method in ['POST', 'DELETE', 'PUT', 'PATCH']:
            timeout = self.write_timeout
        elif method is 'GET':
            timeout = self.read_timeout

        resp = self._make_request(method, url, allow_redirects, timeout,
                                  **kwargs)
        if self._unauthorized(resp):
            try:
                # re-authenticate and attempt one more request
                self.re_authenticate()
                kwargs['headers']['X-Auth-Token'] = self.auth_token
                resp = self._make_request(method, url, allow_redirects,
                                          timeout, **kwargs)
                self._check_status_code(resp, method, **kwargs)
            except exc.KeystoneException as e:
                raise e
        else:
            self._check_status_code(resp, method, **kwargs)
        return resp

    def _unauthorized(self, resp):
        status401 = (resp.status_code == 401)
        status500 = (resp.status_code == 500 and "(HTTP 401)" in resp.content)
        return status401 or status500

    def _check_status_code(self, resp, method, **kwargs):
        if self._unauthorized(resp):
            message = "Unauthorized error"
            raise exc.HTTPUnauthorized(message=message)
        elif 400 <= resp.status_code < 600:
            raise exc.from_response(resp)
        elif resp.status_code in (301, 302, 305):
            # Redirected. Reissue the request to the new location.
            location = resp.headers.get('location')
            if location is None:
                message = "Location not returned with 302"
                raise exc.InvalidEndpoint(message=message)
            elif location.startswith(self.endpoint):
                # shave off the endpoint, it will be prepended when we recurse
                location = location[len(self.endpoint):]
            else:
                message = "Prohibited endpoint redirect %s" % location
                raise exc.InvalidEndpoint(message=message)
            return self._http_request(location, method, **kwargs)
        elif resp.status_code == 300:
            raise exc.from_response(resp)

    def _make_request(self, method, url, allow_redirects, timeout, **kwargs):
        try:
            resp = requests.request(
                method,
                self.endpoint_url + url,
                allow_redirects=allow_redirects,
                timeout=timeout,
                **kwargs)
        except socket.gaierror as e:
            message = ("Error finding address for %(url)s: %(e)s" %
                       {'url': self.endpoint_url + url, 'e': e})
            raise exc.InvalidEndpoint(message=message)
        except (socket.error, socket.timeout) as e:
            endpoint = self.endpoint
            message = ("Error communicating with %(endpoint)s %(e)s" %
                       {'endpoint': endpoint, 'e': e})
            raise exc.CommunicationError(message=message)
        except requests.Timeout as e:
            endpoint = self.endpoint
            message = ("Error %(method)s timeout request to %(endpoint)s %(e)s" %
                       {'method': method, 'endpoint': endpoint, 'e': e})
            raise exc.RequestTimeoutError(message=message)
        except requests.ConnectionError as ex:
            endpoint = self.endpoint
            message = ("Failed to connect to %s, error was %s" % (endpoint, ex.message))
            raise exc.CommunicationError(message=message)
        self.log_http_response(resp)
        return resp

    def credentials_headers(self):
        creds = {}
        if self.username:
            creds['X-Auth-User'] = self.username
        if self.password:
            creds['X-Auth-Key'] = self.password
        return creds

    def json_request(self, method, url, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type', 'application/json')
        kwargs['headers'].setdefault('Accept', 'application/json')

        if 'data' in kwargs:
            kwargs['data'] = jsonutils.dumps(kwargs['data'])

        resp = self._http_request(url, method, **kwargs)
        body = resp.content
        if 'application/json' in resp.headers.get('content-type', ''):
            try:
                body = resp.json()
            except ValueError:
                LOG.error('Could not decode response body as JSON')
        else:
            body = None

        return resp, body

    def raw_request(self, method, url, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type',
                                     'application/octet-stream')
        return self._http_request(url, method, **kwargs)

    def client_request(self, method, url, **kwargs):
        resp, body = self.json_request(method, url, **kwargs)
        return resp

    def head(self, url, **kwargs):
        return self.client_request("HEAD", url, **kwargs)

    def get(self, url, **kwargs):
        return self.client_request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.client_request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.client_request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.raw_request("DELETE", url, **kwargs)

    def patch(self, url, **kwargs):
        return self.client_request("PATCH", url, **kwargs)
