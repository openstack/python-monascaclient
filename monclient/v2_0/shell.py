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

import yaml

from monclient.common import utils
from monclient.openstack.common import jsonutils
from monclient.openstack.common.py3kcompat import urlutils

import monclient.exc as exc

@utils.arg('json_body', metavar='<json body>',
           help='the json body for the http request')
def do_metrics_create(hc, args):
    '''Create one or more metrics.'''
    fields = {'json_body': args.json_body}
    print("in do_metrics_create")


