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
from monascaclient.v2_0 import notificationtypes
from monascaclient.v2_0 import shell


class FakeV2Client(object):

    def __init__(self):
        super(FakeV2Client, self).__init__()
        self.notificationtypes = mock.Mock(
            spec=notificationtypes.NotificationTypesManager)


class TestNotificationsTypesShellV2(base.BaseTestCase):

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_notification_types_list(self, mc):
        mc.return_value = c = FakeV2Client()
        c.notificationtypes.list.return_value = [
            {"type": "WEBHOOK"},
            {"type": "EMAIL"},
            {"type": "PAGERDUTY"}
        ]

        raw_args = []
        name, cmd_clazz = migr.create_command_class('do_notification_type_list',
                                                    shell)
        cmd = cmd_clazz(mock.Mock(), mock.Mock())

        parser = cmd.get_parser(name)
        parsed_args = parser.parse_args(raw_args)
        cmd.run(parsed_args)

        c.notificationtypes.list.assert_called_once()
