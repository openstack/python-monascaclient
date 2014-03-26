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

import re
import six
import sys

import fixtures
import testtools

from keystoneclient.v2_0 import client as ksclient
from monclient.common import http
from monclient import exc
import monclient.shell
from monclient.tests import fakes
from mox3 import mox


class TestCase(testtools.TestCase):

    def set_fake_env(self, fake_env):
        client_env = ('OS_USERNAME', 'OS_PASSWORD', 'OS_TENANT_ID',
                      'OS_TENANT_NAME', 'OS_AUTH_URL', 'OS_REGION_NAME',
                      'OS_AUTH_TOKEN', 'OS_NO_CLIENT_AUTH', 'OS_SERVICE_TYPE',
                      'OS_ENDPOINT_TYPE', 'MON_API_URL')

        for key in client_env:
            self.useFixture(
                fixtures.EnvironmentVariable(key, fake_env.get(key)))

    # required for testing with Python 2.6
    def assertRegexpMatches(self, text, expected_regexp, msg=None):
        """Fail the test unless the text matches the regular expression."""
        if isinstance(expected_regexp, six.string_types):
            expected_regexp = re.compile(expected_regexp)
        if not expected_regexp.search(text):
            msg = msg or "Regexp didn't match"
            msg = '%s: %r not found in %r' % (
                msg, expected_regexp.pattern, text)
            raise self.failureException(msg)

    def shell_error(self, argstr, error_match):
        orig = sys.stderr
        sys.stderr = six.StringIO()
        _shell = monclient.shell.MonShell()
        e = self.assertRaises(Exception, _shell.main, argstr.split())
        self.assertRegexpMatches(e.__str__(), error_match)
        err = sys.stderr.getvalue()
        sys.stderr.close()
        sys.stderr = orig
        return err


class ShellBase(TestCase):

    def setUp(self):
        super(ShellBase, self).setUp()
        self.m = mox.Mox()
        self.m.StubOutWithMock(ksclient, 'Client')
        self.m.StubOutWithMock(http.HTTPClient, 'json_request')
        self.m.StubOutWithMock(http.HTTPClient, 'raw_request')
        self.addCleanup(self.m.VerifyAll)
        self.addCleanup(self.m.UnsetStubs)

        # Some tests set exc.verbose = 1, so reset on cleanup
        def unset_exc_verbose():
            exc.verbose = 0

        self.addCleanup(unset_exc_verbose)

    def shell(self, argstr):
        orig = sys.stdout
        try:
            sys.stdout = six.StringIO()
            _shell = monclient.shell.MonShell()
            _shell.main(argstr.split())
            self.subcommands = _shell.subcommands.keys()
        except SystemExit:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.assertEqual(0, exc_value.code)
        finally:
            out = sys.stdout.getvalue()
            sys.stdout.close()
            sys.stdout = orig

        return out


class ShellTestCommon(ShellBase):

    def setUp(self):
        super(ShellTestCommon, self).setUp()

    def test_help_unknown_command(self):
        self.assertRaises(exc.CommandError, self.shell, 'help foofoo')

    def test_help(self):
        required = [
            '^usage: mon',
            '(?m)^See "mon help COMMAND" for help on a specific command',
        ]
        for argstr in ['--help', 'help']:
            help_text = self.shell(argstr)
            for r in required:
                self.assertRegexpMatches(help_text, r)

    def test_command_help(self):
        output = self.shell('help help')
        self.assertIn('usage: mon help [<subcommand>]', output)
        subcommands = list(self.subcommands)
        for command in subcommands:
            if command.replace('_', '-') == 'bash-completion':
                continue
            output1 = self.shell('help %s' % command)
            output2 = self.shell('%s --help' % command)
            self.assertEqual(output1, output2)
            self.assertRegexpMatches(output1, '^usage: mon %s' % command)

    def test_help_on_subcommand(self):
        required = [
            '^usage: mon metrics-create',
            "(?m)^Create metric",
        ]
        argstrings = [
            'help metrics-create',
        ]
        for argstr in argstrings:
            help_text = self.shell(argstr)
            for r in required:
                self.assertRegexpMatches(help_text, r)


class ShellTestMonCommands(ShellBase):

    def setUp(self):
        super(ShellTestMonCommands, self).setUp()
        self._set_fake_env()

    def _set_fake_env(self):
        fake_env = {
            'OS_USERNAME': 'username',
            'OS_PASSWORD': 'password',
            'OS_TENANT_NAME': 'tenant_name',
            'OS_AUTH_URL': 'http://no.where',
        }
        self.set_fake_env(fake_env)

    def _script_keystone_client(self):
        fakes.script_keystone_client()

    def test_bad_metrics_create_subcommand(self):
        argstrings = [
            'metrics-create --name cindy',
            'metrics-create --value 123',
            'metrics-create',
        ]
        _shell = monclient.shell.MonShell()
        for argstr in argstrings:
            self.assertRaises(SystemExit, _shell.main, argstr.split())

    def test_good_metrics_create_subcommand(self):
        self._script_keystone_client()

        resp = fakes.FakeHTTPResponse(
            204,
            'Created',
            {'location': 'http://no.where/v2.0/metrics'},
            None)
        http.HTTPClient.json_request(
            'POST',
            '/metrics',
            data={'timestamp': 1395691090,
                  'name': 'cindy',
                  'value': 123.0},
            headers={'X-Auth-Key': 'password',
                     'X-Auth-User': 'username'}).AndReturn((resp,
                                                            None))

        self.m.ReplayAll()

        argstrings = [
            'metrics-create --name cindy --value 123 --time 1395691090',
        ]
        for argstr in argstrings:
            retvalue = self.shell(argstr)
            self.assertRegexpMatches(retvalue, "^Success")

    def test_bad_notifications_create_missing_args_subcommand(self):
        argstrings = [
            'notifications-create --name email1 --address cindy.o-neill@hp.com',
        ]
        _shell = monclient.shell.MonShell()
        for argstr in argstrings:
            self.assertRaises(SystemExit, _shell.main, argstr.split())

    def test_bad_notifications_create_type_subcommand(self):
        self._script_keystone_client()
        argstrings = [
            'notifications-create --name email1 --type DOG --address cindy.o-neill@hp.com',
        ]
        self.m.ReplayAll()
        for argstr in argstrings:
            retvalue = self.shell(argstr)
            self.assertRegexpMatches(retvalue, "^Invalid type")

    def test_good_notifications_create_subcommand(self):
        self._script_keystone_client()

        resp = fakes.FakeHTTPResponse(
            201,
            'Created',
            {'location': 'http://no.where/v2.0/notification-methods'},
            None)
        http.HTTPClient.json_request(
            'POST',
            '/notification-methods',
            data={'name': 'email1',
                  'type': 'EMAIL',
                  'address': 'john.doe@hp.com'},
            headers={'X-Auth-Key': 'password',
                     'X-Auth-User': 'username'}).AndReturn((resp, 'id'))

        self.m.ReplayAll()

        argstrings = [
            'notifications-create --name email1 --type EMAIL --address john.doe@hp.com',
        ]
        for argstr in argstrings:
            retvalue = self.shell(argstr)
            self.assertRegexpMatches(retvalue, "id")
