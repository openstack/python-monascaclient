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

from monclient.common import utils
import monclient.exc as exc
from monclient.openstack.common import jsonutils
import time


@utils.arg('--name', metavar='<METRIC_NAME>',
           help='Name of the metric to create.', required=True)
@utils.arg('--dimensions', metavar='<KEY1=VALUE1;KEY2=VALUE2...>',
           help='key value pairs used to create the metric dimensions. '
           'This can be specified multiple times, or once with parameters '
           'separated by a semicolon.',
           action='append')
@utils.arg('--time', metavar='<UNIX_TIMESTAMP>',
           default=time.time(), type=int,
           help='Metric timestamp. Default: current timestamp.')
@utils.arg('--value', metavar='<METRIC_VALUE>',
           default=time.time(), type=float,
           help='Metric value.', required=True)
def do_metrics_create(mc, args):
    '''Create metric.'''
    #print("in do_metrics_create")
    fields = {}
    fields['name'] = args.name
    if args.dimensions:
        fields['dimensions'] = utils.format_parameters(args.dimensions)
    fields['timestamp'] = args.time
    fields['value'] = args.value
    try:
        mc.metrics.create(args.runlocal, **fields)
    except exc.HTTPInternalServerError as e1:
        raise exc.CommandError('HTTPInternalServerError %s' % e1.code)
    except exc.BadRequest as e2:
        raise exc.CommandError('BadRequest %s' % e2.code)
    except exc.Unauthorized as e3:
        raise exc.CommandError('Unauthorized %s' % e3.code)
    except exc.HTTPUnProcessable as e4:
        raise exc.CommandError('UnprocessableEntity %s' % e4.code)
    except Exception:
        print('Command Failed. Please use the -d option for more details.')
        raise
    else:
        print('Successfully created metric')


@utils.arg('--name', metavar='<NOTIFICATION_NAME>',
           help='Name of the notification to create.', required=True)
@utils.arg('--type', metavar='<EMAIL | SMS>',
           help='The notification type.  Types is one of [EMAIL, SMS].',
           required=True)
@utils.arg('--address', metavar='<ADDRESS>',
           help='Depending on the type, a valid EMAIL or SMS Address',
           required=True)
def do_notifications_create(mc, args):
    '''Create notification.'''
    notification_types = ['EMAIL', 'SMS']
    if args.type not in notification_types:
        errmsg = 'Invalid type, not one of [' + \
            ', '.join(notification_types) + ']'
        print(errmsg)
        return
    fields = {}
    fields['name'] = args.name
    fields['type'] = args.type
    fields['address'] = args.address
    try:
        notification = mc.notifications.create(args.runlocal, **fields)
    except exc.HTTPInternalServerError as e1:
        raise exc.CommandError('HTTPInternalServerError %s' % e1.code)
    except exc.BadRequest as e2:
        raise exc.CommandError('BadRequest %s' % e2.code)
    except exc.Unauthorized as e3:
        raise exc.CommandError('Unauthorized %s' % e3.code)
    except exc.HTTPConflict as e4:
        raise exc.CommandError('Conflict %s' % e4.code)
    except Exception:
        print('Command Failed. Please use the -d option for more details.')
        raise
    else:
        print(jsonutils.dumps(notification, indent=2))
