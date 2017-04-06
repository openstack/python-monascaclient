# (C) Copyright 2014-2015 Hewlett Packard Enterprise Development Company LP
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

from __future__ import print_function

import argparse
import logging
import string
import sys
import warnings

import monascaclient
from monascaclient import client as monasca_client
from monascaclient.common import utils
from monascaclient import exc
from monascaclient import ksclient


logger = logging.getLogger(__name__)


class DeprecatedStore(argparse._StoreAction):
    def __init__(self, *args, **kwargs):
        super(DeprecatedStore, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        warnings.filterwarnings(action='default', category=DeprecationWarning, module='.*monascaclient.*')
        warnings.warn("{} is deprecated".format(",".join(self.option_strings)),
                      DeprecationWarning)
        setattr(namespace, self.dest, values)


class MonascaShell(object):

    def get_base_parser(self):
        parser = argparse.ArgumentParser(
            prog='monasca',
            description=__doc__.strip(),
            epilog='See "monasca help COMMAND" '
                   'for help on a specific command.',
            add_help=False,
            # formatter_class=HelpFormatter,
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog,
                max_help_position=29)
        )

        # Global arguments
        parser.add_argument('-h', '--help',
                            action='store_true',
                            help=argparse.SUPPRESS)

        parser.add_argument('-j', '--json',
                            action='store_true',
                            help='output raw json response')

        parser.add_argument('--version',
                            action='version',
                            version=monascaclient.__version__,
                            help="Shows the client version and exits.")

        parser.add_argument('-d', '--debug',
                            default=bool(utils.env('MONASCA_DEBUG')),
                            action='store_true',
                            help='Defaults to env[MONASCA_DEBUG].')

        parser.add_argument('-v', '--verbose',
                            default=False, action="store_true",
                            help="Print more verbose output.")

        parser.add_argument('-k', '--insecure',
                            default=False,
                            action='store_true',
                            help="Explicitly allow the client to perform "
                            "\"insecure\" SSL (https) requests. The server's "
                            "certificate will not be verified against any "
                            "certificate authorities. "
                            "This option should be used with caution.")

        parser.add_argument('--cert-file',
                            help='Path of certificate file to use in SSL '
                            'connection. This file can optionally be '
                            'prepended with the private key.')

        parser.add_argument(
            '--key-file',
            help='Path of client key to use in SSL connection. '
            'This option is not necessary if your key is'
            ' prepended to your cert file.')

        parser.add_argument('--os-cacert',
                            default=utils.env('OS_CACERT'),
                            help='Specify a CA bundle file to use in verifying'
                            ' a TLS (https) server certificate. Defaults to'
                            ' env[OS_CACERT]. Without either of these, the'
                            ' client looks for the default system CA'
                            ' certificates.')

        parser.add_argument('--keystone_timeout',
                            default=20,
                            help='Number of seconds to wait for a response from keystone.')

        parser.add_argument('--os-username',
                            default=utils.env('OS_USERNAME'),
                            help='Defaults to env[OS_USERNAME].')

        parser.add_argument('--os_username',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-password',
                            default=utils.env('OS_PASSWORD'),
                            help='Defaults to env[OS_PASSWORD].')

        parser.add_argument('--os_password',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-user-domain-id',
                            default=utils.env('OS_USER_DOMAIN_ID'),
                            help='Defaults to env[OS_USER_DOMAIN_ID].')

        parser.add_argument('--os-user-domain-name',
                            default=utils.env('OS_USER_DOMAIN_NAME'),
                            help='Defaults to env[OS_USER_DOMAIN_NAME].')

        parser.add_argument('--os-project-id',
                            default=utils.env('OS_PROJECT_ID'),
                            help='Defaults to env[OS_PROJECT_ID].')

        parser.add_argument('--os_project_id',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-project-name',
                            default=utils.env('OS_PROJECT_NAME'),
                            help='Defaults to env[OS_PROJECT_NAME].')

        parser.add_argument('--os_project_name',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-tenant-name',
                            dest='os_project_name',
                            action=DeprecatedStore,
                            default=utils.env('OS_TENANT_NAME'),
                            help='(Deprecated, use --os-project_name) '
                            'Defaults to env[OS_TENANT_NAME].')

        parser.add_argument('--os_tenant_name',
                            dest='os_project_name',
                            action=DeprecatedStore,
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-tenant-id',
                            dest='os_project_id',
                            action=DeprecatedStore,
                            default=utils.env('OS_TENANT_ID'),
                            help='(Deprecated, use --os-project_id) '
                            'Defaults to env[OS_TENANT_ID].')

        parser.add_argument('--os_tenant_id',
                            dest='os_project_id',
                            action=DeprecatedStore,
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-project-domain-id',
                            default=utils.env('OS_PROJECT_DOMAIN_ID'),
                            help='Defaults to env[OS_PROJECT_DOMAIN_ID].')

        parser.add_argument('--os-project-domain-name',
                            default=utils.env('OS_PROJECT_DOMAIN_NAME'),
                            help='Defaults to env[OS_PROJECT_DOMAIN_NAME].')

        parser.add_argument('--os-auth-url',
                            default=utils.env('OS_AUTH_URL'),
                            help='Defaults to env[OS_AUTH_URL].')

        parser.add_argument('--os_auth_url',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-region-name',
                            default=utils.env('OS_REGION_NAME'),
                            help='Defaults to env[OS_REGION_NAME].')

        parser.add_argument('--os_region_name',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-auth-token',
                            default=utils.env('OS_AUTH_TOKEN'),
                            help='Defaults to env[OS_AUTH_TOKEN].')

        parser.add_argument('--os_auth_token',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-no-client-auth',
                            default=utils.env('OS_NO_CLIENT_AUTH'),
                            action='store_true',
                            help="Do not contact keystone for a token. "
                                 "Defaults to env[OS_NO_CLIENT_AUTH].")

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

        parser.add_argument('--os-service-type',
                            default=utils.env('OS_SERVICE_TYPE'),
                            help='Defaults to env[OS_SERVICE_TYPE].')

        parser.add_argument('--os_service_type',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-endpoint-type',
                            default=utils.env('OS_ENDPOINT_TYPE'),
                            help='Defaults to env[OS_ENDPOINT_TYPE].')

        parser.add_argument('--os_endpoint_type',
                            help=argparse.SUPPRESS)

        # In OpenStack, the parameters below are intended for domain-scoping, i.e. authorize
        # the user against a domain instead of a project. Previous versions of the agent used these
        # to qualify the project name, leading to confusion and preventing reuse of typical RC files.
        # Since domain scoping is not supported by Monasca, we can still support the old variable
        # names for the time being. If the project-name is not scoped using the correct project
        # domain name parameter, the code falls back to  the domain scoping parameters.
        parser.add_argument('--os-domain-id',
                            default=utils.env('OS_DOMAIN_ID'),
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-domain-name',
                            default=utils.env('OS_DOMAIN_NAME'),
                            help=argparse.SUPPRESS)

        return parser

    def get_subcommand_parser(self, version):
        parser = self.get_base_parser()

        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')
        submodule = utils.import_versioned_module(version, 'shell')
        self._find_actions(subparsers, submodule)
        self._find_actions(subparsers, self)
        self._add_bash_completion_subparser(subparsers)

        return parser

    def _add_bash_completion_subparser(self, subparsers):
        subparser = subparsers.add_parser(
            'bash_completion',
            add_help=False,
            formatter_class=HelpFormatter
        )
        self.subcommands['bash_completion'] = subparser
        subparser.set_defaults(func=self.do_bash_completion)

    def _find_actions(self, subparsers, actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            # I prefer to be hyphen-separated instead of underscores.
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            help = desc.strip().split('\n')[0]
            arguments = getattr(callback, 'arguments', [])

            subparser = subparsers.add_parser(command,
                                              help=help,
                                              description=desc,
                                              add_help=False,
                                              formatter_class=HelpFormatter)
            subparser.add_argument('-h', '--help',
                                   action='help',
                                   help=argparse.SUPPRESS)
            self.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)

    def _setup_logging(self, debug):
        log_lvl = logging.DEBUG if debug else logging.ERROR
        logging.basicConfig(
            format="%(levelname)s (%(module)s:%(lineno)d) %(message)s",
            level=log_lvl)

    def _setup_verbose(self, verbose):
        if verbose:
            exc.verbose = 1

    def main(self, argv):
        # Parse args once to find version
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        self._setup_logging(options.debug)
        self._setup_verbose(options.verbose)

        # build available subcommands based on version
        api_version = options.monasca_api_version
        subcommand_parser = self.get_subcommand_parser(api_version)
        self.parser = subcommand_parser

        # Handle top-level --help/-h before attempting to parse
        # a command off the command line
        if not args and options.help or not argv:
            self.do_help(options)
            return 0

        # Parse args again and call whatever callback was selected
        args = subcommand_parser.parse_args(argv)

        # Short-circuit and deal with help command right away.
        if args.func == self.do_help:
            self.do_help(args)
            return 0
        elif args.func == self.do_bash_completion:
            self.do_bash_completion(args)
            return 0

        if not args.os_username and not args.os_auth_token:
            raise exc.CommandError("You must provide a username via"
                                   " either --os-username or env[OS_USERNAME]"
                                   " or a token via --os-auth-token or"
                                   " env[OS_AUTH_TOKEN]")

        if not args.os_password and not args.os_auth_token:
            raise exc.CommandError("You must provide a password via"
                                   " either --os-password or env[OS_PASSWORD]"
                                   " or a token via --os-auth-token or"
                                   " env[OS_AUTH_TOKEN]")

        if args.os_no_client_auth:
            if not args.monasca_api_url:
                raise exc.CommandError("If you specify --os-no-client-auth"
                                       " you must specify a Monasca API URL"
                                       " via either --monasca-api-url or"
                                       " env[MONASCA_API_URL]")
        else:
            if not args.os_auth_url:
                raise exc.CommandError("You must provide an auth url via"
                                       " either --os-auth-url or via"
                                       " env[OS_AUTH_URL]")

        if args.os_auth_url and 'v2.0' in args.os_auth_url:
            args.os_auth_url = string.replace(args.os_auth_url, 'v2.0', 'v3')

        kwargs = {
            'username': args.os_username,
            'password': args.os_password,
            'token': args.os_auth_token,
            'auth_url': args.os_auth_url,
            'service_type': args.os_service_type,
            'endpoint_type': args.os_endpoint_type,
            'os_cacert': args.os_cacert,
            'user_domain_id': args.os_user_domain_id,
            'user_domain_name': args.os_user_domain_name,
            'project_id': args.os_project_id,
            'project_name': args.os_project_name,
            #  if project name is not scoped, fall back to  previous behaviour (see above)
            'project_domain_id': args.os_project_domain_id if args.os_project_domain_id else args.os_domain_id,
            'project_domain_name': args.os_project_domain_name if args.os_project_domain_name else args.os_domain_name,
            'insecure': args.insecure,
            'region_name': args.os_region_name,
            'keystone_timeout': args.keystone_timeout
        }

        endpoint = args.monasca_api_url

        if not args.os_no_client_auth:
            _ksclient = ksclient.KSClient(**kwargs)
            if args.os_auth_token:
                token = args.os_auth_token
            else:
                try:
                    token = _ksclient.token
                except exc.CommandError:
                    raise exc.CommandError(
                        "User does not have a default project. "
                        "You must provide a project id using "
                        "--os-project-id or via env[OS_PROJECT_ID], "
                        "or you must provide a project name using "
                        "--os-project-name or via env[OS_PROJECT_NAME] "
                        "and a project domain using --os-project-domain-name, via "
                        "env[OS_PROJECT_DOMAIN_NAME],  using --os-project-domain-id or "
                        "via env[OS_PROJECT_DOMAIN_ID]")

            kwargs = {
                'token': token,
                'insecure': args.insecure,
                'os_cacert': args.os_cacert,
                'cert_file': args.cert_file,
                'key_file': args.key_file,
                'username': args.os_username,
                'password': args.os_password,
                'service_type': args.os_service_type,
                'endpoint_type': args.os_endpoint_type,
                'auth_url': args.os_auth_url,
                'keystone_timeout': args.keystone_timeout
            }

            if args.os_user_domain_name:
                kwargs['user_domain_name'] = args.os_user_domain_name
            if args.os_user_domain_id:
                kwargs['user_domain_id'] = args.os_user_domain_id
            if args.os_region_name:
                kwargs['region_name'] = args.os_region_name
            if args.os_project_name:
                kwargs['project_name'] = args.os_project_name
            if args.os_project_id:
                kwargs['project_id'] = args.os_project_id
            # Monasca API uses domain_id/name for project_domain_id/name
            # We cannot change this and therefore still use the misleading parameter names
            if args.os_domain_name:
                kwargs['domain_name'] = args.os_project_domain_name if args.os_project_domain_name \
                    else args.os_domain_name
            if args.os_domain_id:
                kwargs['domain_id'] = args.os_project_domain_id if args.os_project_domain_id \
                    else args.os_domain_id

            if not endpoint:
                endpoint = _ksclient.monasca_url

        client = monasca_client.Client(api_version, endpoint, **kwargs)

        args.func(client, args)

    def do_bash_completion(self, args):
        """Prints all of the commands and options to stdout.

        The monasca.bash_completion script doesn't have to hard code them.
        """
        commands = set()
        options = set()
        for sc_str, sc in self.subcommands.items():
            commands.add(sc_str)
            for option in list(sc._optionals._option_string_actions):
                options.add(option)

        commands.remove('bash-completion')
        commands.remove('bash_completion')
        print(' '.join(commands | options))

    @utils.arg('command', metavar='<subcommand>', nargs='?',
               help='Display help for <subcommand>.')
    def do_help(self, args):
        """Display help about this program or one of its subcommands."""
        if getattr(args, 'command', None):
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise exc.CommandError("'%s' is not a valid subcommand" %
                                       args.command)
        else:
            self.parser.print_help()


class HelpFormatter(argparse.HelpFormatter):

    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(HelpFormatter, self).start_section(heading)


def main(args=None):
    try:
        if args is None:
            args = sys.argv[1:]

        MonascaShell().main(args)
    except Exception as e:
        if '--debug' in args or '-d' in args:
            raise
        else:
            print(e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
