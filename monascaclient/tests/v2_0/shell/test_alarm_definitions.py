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
from monascaclient.v2_0 import alarm_definitions as ad
from monascaclient.v2_0 import shell


class FakeV2Client(object):
    def __init__(self):
        super(FakeV2Client, self).__init__()
        self.alarm_definitions = mock.Mock(
            spec=ad.AlarmDefinitionsManager)


class TestAlarmDefinitionShellV2(base.BaseTestCase):

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_should_update(self, mc):
        mc.return_value = c = FakeV2Client()

        ad_id = '0495340b-58fd-4e1c-932b-5e6f9cc96490'
        ad_name = 'alarm_name'
        ad_desc = 'test_alarm_definition'
        ad_expr = 'avg(Test_Metric_1)>=10'
        ad_action_id = '16012650-0b62-4692-9103-2d04fe81cc93'
        ad_action_enabled = 'True'
        ad_match_by = 'hostname'
        ad_severity = 'CRITICAL'

        raw_args = [
            ad_id, ad_name, ad_desc, ad_expr,
            ad_action_id, ad_action_id, ad_action_id, ad_action_enabled,
            ad_match_by, ad_severity
        ]
        name, cmd_clazz = migr.create_command_class(
            'do_alarm_definition_update',
            shell
        )
        cmd = cmd_clazz(mock.Mock(), mock.Mock())

        parser = cmd.get_parser(name)
        parsed_args = parser.parse_args(raw_args)
        cmd.run(parsed_args)

        c.alarm_definitions.update.assert_called_once_with(
            actions_enabled=True,
            alarm_actions=[ad_action_id],
            alarm_id=ad_id,
            description=ad_desc,
            expression=ad_expr,
            match_by=[ad_match_by],
            name=ad_name,
            ok_actions=[ad_action_id],
            severity=ad_severity,
            undetermined_actions=[ad_action_id]
        )

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_alarm_definitions_list(self, mc):
        mc.return_value = c = FakeV2Client()

        c.alarm_definitions.list.return_value = [{
            "name": "ntp_sync_check",
            "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "expression": "(max(ntp.offset{}, deterministic)>=1)",
            "match_by": ['hostname'],
            "description": "NTP time sync check",
            "actions_enabled": True,
            "deterministic": True,
            "alarm_actions": ['aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'],
            "ok_actions": [],
            "undetermined_actions": [],
            "severity": "HIGH",
        }]

        name, cmd_class = migr.create_command_class(
            'do_alarm_definition_list',
            shell
        )
        cmd = cmd_class(mock.Mock(), mock.Mock())

        parser = cmd.get_parser(name)
        raw_args = []
        parsed_args = parser.parse_args(raw_args)
        cmd.run(parsed_args)

        c.alarm_definitions.list.assert_called_once()

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_should_patch_name(self, mc):
        ad_id = '0495340b-58fd-4e1c-932b-5e6f9cc96490'
        ad_name = 'patch_name'

        raw_args = '{0} --name {1}'.format(ad_id, ad_name).split(' ')
        self._patch_test(mc, raw_args, alarm_id=ad_id, name=ad_name)

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_should_patch_actions(self, mc):
        ad_id = '0495340b-58fd-4e1c-932b-5e6f9cc96490'
        ad_action_id = '16012650-0b62-4692-9103-2d04fe81cc93'

        actions = ['alarm-actions', 'ok-actions',
                   'undetermined-actions']
        for action in actions:
            raw_args = ('{0} --{1} {2}'.format(ad_id, action, ad_action_id)
                        .split(' '))
            self._patch_test(mc, raw_args, **{
                'alarm_id': ad_id,
                action.replace('-', '_'): [ad_action_id]
            })

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_should_patch_severity(self, mc):
        ad_id = '0495340b-58fd-4e1c-932b-5e6f9cc96490'

        severity_types = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        for st in severity_types:
            raw_args = ('{0} --severity {1}'.format(ad_id, st)
                        .split(' '))
            self._patch_test(mc, raw_args, alarm_id=ad_id, severity=st)

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_should_not_patch_unknown_severity(self, mc):
        ad_id = '0495340b-58fd-4e1c-932b-5e6f9cc96490'

        st = 'foo'
        raw_args = ('{0} --severity {1}'.format(ad_id, st)
                    .split(' '))
        self._patch_test(mc, raw_args, called=False)

    @staticmethod
    def _patch_test(mc, args, called=True, **kwargs):
        mc.return_value = c = FakeV2Client()

        name, cmd_clazz = migr.create_command_class(
            'do_alarm_definition_patch',
            shell
        )

        cmd = cmd_clazz(mock.Mock(), mock.Mock())

        parser = cmd.get_parser(name)
        parsed_args = parser.parse_args(args)
        cmd.run(parsed_args)

        if called:
            c.alarm_definitions.patch.assert_called_once_with(**kwargs)
        else:
            c.alarm_definitions.patch.assert_not_called()
