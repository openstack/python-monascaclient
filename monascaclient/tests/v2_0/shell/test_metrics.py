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
from monascaclient.v2_0 import metrics
from monascaclient.v2_0 import shell


class FakeV2Client(object):
    def __init__(self):
        super(FakeV2Client, self).__init__()
        self.metrics = mock.Mock(spec=metrics.MetricsManager)


class TestMetricsShellV2(base.BaseTestCase):

    def test_bad_metrics(self):
        raw_args_list = [
            ['metric1'],
            ['123'],
            ['']
        ]
        name, cmd_clazz = migr.create_command_class('do_metric_create',
                                                    shell)

        for raw_args in raw_args_list:
            cmd = cmd_clazz(mock.Mock(), mock.Mock())
            parser = cmd.get_parser(name)
            self.assertRaises(SystemExit, parser.parse_args, raw_args)

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_metric_create(self, mc):
        mc.return_value = c = FakeV2Client()

        raw_args = 'metric1 123 --time 1395691090'.split(' ')
        name, cmd_clazz = migr.create_command_class('do_metric_create',
                                                    shell)
        cmd = cmd_clazz(mock.Mock(), mock.Mock())

        parser = cmd.get_parser(name)
        parsed_args = parser.parse_args(raw_args)
        cmd.run(parsed_args)

        data = {'timestamp': 1395691090,
                'name': 'metric1',
                'value': 123.0}

        c.metrics.create.assert_called_once_with(**data)

    @mock.patch('monascaclient.osc.migration.make_client')
    def test_metric_create_with_project_id(self, mc):
        mc.return_value = c = FakeV2Client()

        project_id = 'd48e63e76a5c4e05ba26a1185f31d4aa'
        raw_args = ('metric1 123 --time 1395691090 --project-id %s'
                    % project_id).split(' ')
        name, cmd_clazz = migr.create_command_class('do_metric_create',
                                                    shell)
        cmd = cmd_clazz(mock.Mock(), mock.Mock())

        parser = cmd.get_parser(name)
        parsed_args = parser.parse_args(raw_args)
        cmd.run(parsed_args)

        data = {'timestamp': 1395691090,
                'name': 'metric1',
                'tenant_id': project_id,
                'value': 123.0}

        c.metrics.create.assert_called_once_with(**data)
