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

import mock

from oslotest import base

from monascaclient.osc import migration as migr
from monascaclient.v2_0 import notifications
from monascaclient.v2_0 import shell


class FakeV2Client(object):

    def __init__(self):
        super(FakeV2Client, self).__init__()
        self.notifications = mock.Mock(spec=notifications.NotificationsManager)


class TestNotificationsShellV2(base.BaseTestCase):

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_notification_create_email(self, mc):
        mc.return_value = c = FakeV2Client()

        raw_args = ['email1', 'EMAIL', 'john.doe@hp.com']
        name, cmd_clazz = migr.create_command_class('do_notification_create',
                                                    shell)
        cmd = cmd_clazz(mock.Mock(), mock.Mock())

        parser = cmd.get_parser(name)
        parsed_args = parser.parse_args(raw_args)
        cmd.run(parsed_args)

        data = {'name': 'email1',
                'type': 'EMAIL',
                'address': 'john.doe@hp.com'}

        c.notifications.create.assert_called_once_with(**data)

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_notification_create_webhook(self, mc):
        mc.return_value = c = FakeV2Client()

        raw_args = ['mypost', 'WEBHOOK', 'http://localhost:8080']
        name, cmd_clazz = migr.create_command_class('do_notification_create',
                                                    shell)
        cmd = cmd_clazz(mock.Mock(), mock.Mock())

        parser = cmd.get_parser(name)
        parsed_args = parser.parse_args(raw_args)
        cmd.run(parsed_args)

        data = {'name': 'mypost',
                'type': 'WEBHOOK',
                'address': 'http://localhost:8080'}

        c.notifications.create.assert_called_once_with(**data)

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_good_notifications_patch(self, mc):
        args = '--type EMAIL --address john.doe@hpe.com --period 0'
        data = {'type': 'EMAIL',
                'address': 'john.doe@hpe.com',
                'period': 0}
        self._patch_test(mc, args, data)

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_good_notifications_patch_just_name(self, mc):
        name = 'fred'
        args = '--name ' + name
        data = {'name': name}
        self._patch_test(mc, args, data)

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_good_notifications_patch_just_address(self, mc):
        address = 'fred@fl.com'
        args = '--address ' + address
        data = {'address': address}
        self._patch_test(mc, args, data)

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_good_notifications_patch_just_period(self, mc):
        period = 0
        args = '--period ' + str(period)
        data = {'period': period}
        self._patch_test(mc, args, data)

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_bad_notifications_patch(self, mc):
        mc.return_value = c = FakeV2Client()

        id_str = '0495340b-58fd-4e1c-932b-5e6f9cc96490'
        raw_args = ('{0} --type EMAIL --address john.doe@hpe.com '
                    '--period 60').format(id_str).split(' ')
        name, cmd_clazz = migr.create_command_class('do_notification_patch',
                                                    shell)
        cmd = cmd_clazz(mock.Mock(), mock.Mock())

        parser = cmd.get_parser(name)
        parsed_args = parser.parse_args(raw_args)
        cmd.run(parsed_args)

        c.notifications.patch.assert_not_called()

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_good_notifications_update(self, mc):
        mc.return_value = c = FakeV2Client()

        id_str = '0495340b-58fd-4e1c-932b-5e6f9cc96491'
        raw_args = ('{0} notification_updated_name '
                    'EMAIL john.doe@hpe.com 0').format(id_str).split(' ')
        name, cmd_clazz = migr.create_command_class('do_notification_update',
                                                    shell)
        cmd = cmd_clazz(mock.Mock(), mock.Mock())

        parser = cmd.get_parser(name)
        parsed_args = parser.parse_args(raw_args)

        cmd.run(parsed_args)

        data = {
            'name': 'notification_updated_name',
            'type': 'EMAIL',
            'address': 'john.doe@hpe.com',
            'period': 0,
            'notification_id': id_str
        }

        c.notifications.update.assert_called_once_with(**data)

    @staticmethod
    def _patch_test(mc, args, data):
        mc.return_value = c = FakeV2Client()

        id_str = '0495340b-58fd-4e1c-932b-5e6f9cc96490'
        raw_args = '{0} {1}'.format(id_str, args).split(' ')
        name, cmd_clazz = migr.create_command_class('do_notification_patch',
                                                    shell)
        cmd = cmd_clazz(mock.Mock(), mock.Mock())

        parser = cmd.get_parser(name)
        parsed_args = parser.parse_args(raw_args)
        cmd.run(parsed_args)

        # add notification_id to data
        data['notification_id'] = id_str

        c.notifications.patch.assert_called_once_with(**data)
