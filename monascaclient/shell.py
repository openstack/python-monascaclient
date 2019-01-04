# (C) Copyright 2014-2015 Hewlett Packard Enterprise Development Company LP
# Copyright 2017 Fujitsu LIMITED
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

"""
Command-line interface to the monasca-client API.
"""

import argparse
import locale
import sys

from osc_lib.api import auth
from osc_lib.cli import client_config as cloud_config
from osc_lib import shell
from osc_lib import utils
from oslo_utils import importutils
import six

from monascaclient.osc import migration
from monascaclient import version as mc_version


class MonascaShell(shell.OpenStackShell):
    def __init__(self):
        super(MonascaShell, self).__init__(
            description=__doc__.strip(),
            version=mc_version.version_string
        )
        self.cloud_config = None

    def initialize_app(self, argv):
        super(MonascaShell, self).initialize_app(argv)
        self.cloud_config = cloud_config.OSC_Config(
            override_defaults={
                'interface': None,
                'auth_type': self._auth_type,
            },
        )

    def build_option_parser(self, description, version):
        parser = super(MonascaShell, self).build_option_parser(
            description,
            version
        )
        parser.set_defaults(cloud=None)
        parser = auth.build_auth_plugins_option_parser(parser)
        parser = self._append_monasca_args(parser)
        return parser

    @staticmethod
    def _append_monasca_args(parser):
        parser.add_argument('--monasca-api-url',
                            default=utils.env('MONASCA_API_URL'),
                            help='Defaults to env[MONASCA_API_URL].')
        parser.add_argument('--monasca_api_url',
                            help=argparse.SUPPRESS)
        parser.add_argument('--monasca-api-version',
                            default=utils.env(
                                'MONASCA_API_VERSION',
                                default='2_0'),
                            help='Defaults to env[MONASCA_API_VERSION] or 2_0')
        parser.add_argument('--monasca_api_version',
                            help=argparse.SUPPRESS)
        return parser

    def _load_commands(self):
        version = self.options.monasca_api_version

        submodule = importutils.import_versioned_module('monascaclient',
                                                        version,
                                                        'shell')

        self._find_actions(submodule)

    def _find_actions(self, actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            name, clazz = migration.create_command_class(attr, actions_module)

            if 'help' == name:
                # help requires no auth
                clazz.auth_required = False

            self.command_manager.add_command(name, clazz)


def main(args=None):
    try:
        if args is None:
            args = sys.argv[1:]
            if six.PY2:
                # Emulate Py3, decode argv into Unicode based on locale so that
                # commands always see arguments as text instead of binary data
                encoding = locale.getpreferredencoding()
                if encoding:
                    args = map(lambda arg: arg.decode(encoding), args)
        return MonascaShell().run(args)
    except Exception as e:
        if '--debug' in args or '-d' in args:
            raise
        else:
            print(e)
            sys.exit(1)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
