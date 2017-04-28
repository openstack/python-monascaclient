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

import logging
import six

from osc_lib.command import command
from osc_lib import utils

from monascaclient import version

LOG = logging.getLogger(__name__)

# NOTE(trebskit) this will be moved to another module
# once initial migration is up
# the point is to show how many code can we spare
# in order to get the client working with minimum effort needed
VERSION_MAP = {
    '2_0': 'monascaclient.v2_0.client.Client'
}


def make_client(api_version, session=None,
                endpoint=None, service_type='monitoring'):
    """Returns an monitoring API client."""

    client_cls = utils.get_client_class('monitoring', api_version, VERSION_MAP)
    c = client_cls(
        session=session,
        service_type=service_type,
        endpoint=endpoint,
        app_name='monascaclient',
        app_version=version.version_string,
    )

    return c


def create_command_class(name, func_module):
    """Dynamically creates subclass of MigratingCommand.

    Method takes name of the function, module it is part of
    and builds the subclass of :py:class:`MigratingCommand`.
    Having a subclass of :py:class:`cliff.command.Command` is mandatory
    for the osc-lib integration.

    :param name: name of the function
    :type name: basestring
    :param func_module: the module function is part of
    :type func_module: module
    :return: command name, subclass of :py:class:`MigratingCommand`
    :rtype: tuple(basestring, class)

    """

    cmd_name = name[3:].replace('_', '-')
    callback = getattr(func_module, name)
    desc = callback.__doc__ or ''
    help = desc.strip().split('\n')[0]

    arguments = getattr(callback, 'arguments', [])

    body = {
        '_args': arguments,
        '_callback': staticmethod(callback),
        '_description': desc,
        '_epilog': desc,
        '_help': help
    }

    claz = type('%sCommand' % cmd_name.title().replace('-', ''),
                (MigratingCommand,), body)

    return cmd_name, claz


class MigratingCommandMeta(command.CommandMeta):
    """Overwrite module name based on osc_lib.CommandMeta requirements."""

    def __new__(mcs, name, bases, cls_dict):
        # NOTE(trebskit) little dirty, but should suffice for migration period
        cls_dict['__module__'] = 'monascaclient.v2_0.shell'
        return super(MigratingCommandMeta, mcs).__new__(mcs, name,
                                                        bases, cls_dict)


@six.add_metaclass(MigratingCommandMeta)
class MigratingCommand(command.Command):
    """MigratingCommand is temporary command.

    MigratingCommand allows to map function defined
    shell commands from :py:module:`monascaclient.v2_0.shell`
    into :py:class:`command.Command` instances.

    Note:
        This class is temporary solution during migrating
        to osc_lib and will be removed when all
        shell commands are migrated to cliff commands.

    """

    _help = None
    _args = None
    _callback = None

    def __init__(self, app, app_args, cmd_name=None):
        super(MigratingCommand, self).__init__(app, app_args, cmd_name)
        self._client = None
        self._endpoint = None

    def take_action(self, parsed_args):
        return self._callback(self.mon_client, parsed_args)

    def get_parser(self, prog_name):
        parser = super(MigratingCommand, self).get_parser(prog_name)
        for (args, kwargs) in self._args:
            parser.add_argument(*args, **kwargs)
        parser.add_argument('-j', '--json',
                            action='store_true',
                            help='output raw json response')
        return parser

    @property
    def mon_client(self):
        if not self._client:
            self.log.debug('Initializing mon-client')
            self._client = make_client(api_version=self.mon_version,
                                       endpoint=self.mon_url,
                                       session=self.app.client_manager.session)
        return self._client

    @property
    def mon_version(self):
        return self.app_args.monasca_api_version

    @property
    def mon_url(self):
        if self._endpoint:
            return self._endpoint

        app_args = self.app_args
        cm = self.app.client_manager

        endpoint = app_args.monasca_api_url

        if not endpoint:
            req_data = {
                'service_type': 'monitoring',
                'region_name': cm.region_name,
                'interface': cm.interface,
            }
            LOG.debug('Discovering monasca endpoint using %s' % req_data)
            endpoint = cm.get_endpoint_for_service_type(**req_data)
        else:
            LOG.debug('Using supplied endpoint=%s' % endpoint)

        self._endpoint = endpoint
        return self._endpoint
