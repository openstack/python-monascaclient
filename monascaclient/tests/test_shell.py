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

import mock

from oslotest import base

from monascaclient import shell


class TestMonascaShell(base.BaseTestCase):

    @mock.patch('monascaclient.shell.auth')
    def test_should_use_auth_plugin_option_parser(self, auth):
        auth.build_auth_plugins_option_parser = apop = mock.Mock()
        shell.MonascaShell().run([])
        apop.assert_called_once()

    def test_should_specify_monasca_args(self):
        expected_args = [
            '--monasca-api-url',
            '--monasca-api-version',
            '--monasca_api_url',
            '--monasca_api_version',
        ]

        parser = mock.Mock()
        parser.add_argument = aa = mock.Mock()
        shell.MonascaShell._append_monasca_args(parser)

        aa.assert_called()
        for mc in aa.mock_calls:
            name = mc[1][0]
            self.assertIn(name, expected_args)

    @mock.patch('monascaclient.shell.importutils')
    def test_should_load_commands_based_on_api_version(self, iu):
        iu.import_versioned_module = ivm = mock.Mock()

        instance = shell.MonascaShell()
        instance.options = mock.Mock()
        instance.options.monasca_api_version = version = mock.Mock()

        instance._find_actions = mock.Mock()

        instance._load_commands()

        ivm.assert_called_once_with('monascaclient', version, 'shell')
