# (C) Copyright 2014-2017 Hewlett Packard Enterprise Development LP
# Copyright 2017 FUJITSU LIMITED
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

import warnings

import mock
from oslotest import base

from monascaclient import client


class TestMonascaClient(base.BaseTestCase):

    @mock.patch('monascaclient.client.migration')
    @mock.patch('monascaclient.client._get_auth_handler')
    @mock.patch('monascaclient.client._get_session')
    def test_should_warn_when_passing_args(self, _, __, ___):

        api_version = mock.Mock()
        endpoint = mock.Mock()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            client.Client(api_version, endpoint)

            self.assertEqual(1, len(w))
            self.assertEqual(DeprecationWarning, w[0].category)
            self.assertRegex(
                str(w[0].message),
                'explicit configuration of the client using'
            )

    @mock.patch('monascaclient.client.migration')
    @mock.patch('monascaclient.client._get_auth_handler')
    @mock.patch('monascaclient.client._get_session')
    def test_should_not_warn_when_passing_no_args(self, _, __, ___):
        api_version = mock.Mock()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            client.Client(api_version)
            self.assertEqual(0, len(w))

    @mock.patch('monascaclient.client.migration')
    @mock.patch('monascaclient.client._get_auth_handler')
    @mock.patch('monascaclient.client._get_session')
    def test_should_override_endpoint_if_passed_as_arg(self, get_session,
                                                       get_auth, _):
        api_version = mock.Mock()
        endpoint = mock.Mock()
        endpoint_fake = mock.Mock()
        auth_val = mock.Mock()

        get_auth.return_value = auth_val

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            client.Client(api_version, endpoint, endpoint=endpoint_fake)
            self.assertEqual(1, len(w))

        get_auth.assert_called_once_with({
            'endpoint': endpoint
        })
        get_session.assert_called_once_with(auth_val, {
            'endpoint': endpoint
        })

    @mock.patch('monascaclient.client.migration')
    @mock.patch('monascaclient.client._get_auth_handler')
    @mock.patch('monascaclient.client._get_session')
    def test_should_override_tenant_name_with_project_name(self,
                                                           _,
                                                           get_auth,
                                                           __):
        api_version = mock.Mock()
        auth_val = mock.Mock()
        tenant_name = mock.Mock()
        project_name = tenant_name

        get_auth.return_value = auth_val

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            client.Client(api_version, tenant_name=tenant_name)

            self.assertEqual(1, len(w))
            self.assertEqual(DeprecationWarning, w[0].category)
            self.assertRegex(
                str(w[0].message),
                'Usage of tenant_name has been deprecated in favour '
            )

        get_auth.assert_called_once_with({
            'project_name': project_name
        })

    @mock.patch('monascaclient.client.migration')
    @mock.patch('monascaclient.client._get_auth_handler')
    @mock.patch('monascaclient.client._get_session')
    def test_should_override_insecure_with_negated_verify(self,
                                                          _,
                                                          get_auth,
                                                          __):
        api_version = mock.Mock()
        auth_val = mock.Mock()
        get_auth.return_value = auth_val

        for insecure in [True, False]:
            warnings.resetwarnings()
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                client.Client(api_version, insecure=insecure)

                self.assertEqual(1, len(w))
                self.assertEqual(DeprecationWarning, w[0].category)
                self.assertRegex(
                    str(w[0].message),
                    'Usage of insecure has been deprecated in favour of'
                )

            get_auth.assert_called_once_with({
                'verify': not insecure
            })
            get_auth.reset_mock()

    @mock.patch('monascaclient.client.migration')
    @mock.patch('monascaclient.client._get_auth_handler')
    @mock.patch('monascaclient.client._get_session')
    def test_should_reuse_the_session_if_initialized_with_one(self,
                                                              get_session,
                                                              get_auth,
                                                              _):
        from keystoneauth1 import session as k_session

        api_version = mock.Mock()
        session = mock.Mock(spec=k_session.Session)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            client.Client(api_version, session=session)
            self.assertEqual(0, len(w))

        get_auth.assert_not_called()
        get_session.assert_not_called()

    @mock.patch('monascaclient.client.migration')
    @mock.patch('monascaclient.client._get_auth_handler')
    @mock.patch('monascaclient.client._get_session')
    def test_should_error_if_session_is_not_in_correct_type(self,
                                                            _,
                                                            __,
                                                            ___):

        api_version = mock.Mock()
        for cls in [str, int, float]:
            session = mock.Mock(spec=cls)
            self.assertRaises(RuntimeError, client.Client,
                              api_version, session=session)
