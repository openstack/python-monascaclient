# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import time
from monclient.openstack.common import jsonutils
from monclient.openstack.common.py3kcompat import urlutils
from monclient.common import utils
import monclient.exc as exc


@utils.arg('-n', '--name', metavar='<METRIC_NAME>',
           help='Name of the metric to create.', required=True)
@utils.arg('-d', '--dimensions', metavar='<KEY1=VALUE1;KEY2=VALUE2...>',
           help='key value pairs used to create the metric dimensions. '
           'This can be specified multiple times, or once with parameters '
           'separated by a semicolon.',
           action='append')
@utils.arg('-t', '--time', metavar='<UNIX_TIMESTAMP>',
           default=time.time(), type=int,
           help='Metric timestamp. Default: current timestamp.')
@utils.arg('-v', '--value', metavar='<METRIC_VALUE>',
           default=time.time(), type=float,
           help='Metric value.', required=True)
def do_metrics_create(mc, args):
    '''Create metric.'''
    print("in do_metrics_create")
    fields = {}
    fields['name'] = args.name
    if args.dimensions:
        fields['dimensions'] = utils.format_parameters(args.dimensions)
    fields['timestamp'] = args.time
    fields['value'] = args.value
    resp = mc.metrics.create(args.runlocal, **fields)
    print('Successfully created metric')
