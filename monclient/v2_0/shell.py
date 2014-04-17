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


@utils.arg('name', metavar='<METRIC_NAME>',
           help='Name of the metric to create.')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1>',
           help='key value pair used to create a metric dimension. '
           'This can be specified multiple times.',
           action='append')
@utils.arg('--time', metavar='<UNIX_TIMESTAMP>',
           default=time.time(), type=int,
           help='Metric timestamp. Default: current timestamp.')
@utils.arg('value', metavar='<METRIC_VALUE>',
           default=time.time(), type=float,
           help='Metric value.')
def do_metric_create(mc, args):
    '''Create metric.'''
    fields = {}
    fields['name'] = args.name
    if args.dimensions:
        fields['dimensions'] = utils.format_parameters(args.dimensions)
    fields['timestamp'] = args.time
    fields['value'] = args.value
    try:
        mc.metrics.create(args, **fields)
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


@utils.arg('--name', metavar='<METRIC_NAME>',
           help='Name of the metric to list.')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1>',
           help='key value pair used to specify a dimension. '
           'This can be specified multiple times.',
           action='append')
def do_metric_list(mc, args):
    '''List metrics for this tenant.'''
    fields = {}
    if args.name:
        fields['name'] = args.name
    if args.dimensions:
        fields['dimensions'] = utils.format_parameters(args.dimensions)
        if 'name' not in fields:
            print('--name is required when --dimensions are specified.')
            return
    try:
        metric = mc.metrics.list(args, **fields)
    except exc.HTTPInternalServerError as e1:
        raise exc.CommandError('HTTPInternalServerError %s' % e1.code)
    except exc.BadRequest as e2:
        raise exc.CommandError('BadRequest %s' % e2.code)
    except exc.Unauthorized as e3:
        raise exc.CommandError('Unauthorized %s' % e3.code)
    except exc.HTTPNotFound as e4:
        raise exc.CommandError('Not Found %s' % e4.code)
    except Exception:
        print('Command Failed. Please use the -d option for more details.')
        raise
    else:
        cols = ['name', 'dimensions']
        formatters = {
            'name': lambda x: x['name'],
            'dimensions': lambda x: utils.format_dict(x['dimensions']),
        }
        if isinstance(metric, list):
            # print the list
            utils.print_list(metric, cols, formatters=formatters, sortby=0)
        else:
            # add the dictionary to a list, so print_list works
            metric_list = list()
            metric_list.append(metric)
            utils.print_list(
                metric_list,
                cols,
                formatters=formatters,
                sortby=0)


@utils.arg('name', metavar='<METRIC_NAME>',
           help='Name of the metric to list measurements.')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1>',
           help='key value pair used to specify a dimension. '
           'This can be specified multiple times.',
           action='append')
@utils.arg('starttime', metavar='<UTC_START_TIME>',
           help='measurements >= UTC time. format: 2014-01-01T00:00:00Z.')
@utils.arg('--endtime', metavar='<UTC_END_TIME>',
           help='measurements <= UTC time. format: 2014-01-01T00:00:00Z.')
def do_measurement_list(mc, args):
    '''List measurements for the specified metric.'''
    fields = {}
    fields['name'] = args.name
    if args.dimensions:
        fields['dimensions'] = utils.format_parameters(args.dimensions)
    fields['start_time'] = args.starttime
    if args.endtime:
        fields['end_time'] = args.endtime
    try:
        metric = mc.metrics.list_measurements(args, **fields)
    except exc.HTTPInternalServerError as e1:
        raise exc.CommandError('HTTPInternalServerError %s' % e1.code)
    except exc.BadRequest as e2:
        raise exc.CommandError('BadRequest %s' % e2.code)
    except exc.Unauthorized as e3:
        raise exc.CommandError('Unauthorized %s' % e3.code)
    except exc.HTTPNotFound as e4:
        raise exc.CommandError('Not Found %s' % e4.code)
    except Exception:
        print('Command Failed. Please use the -d option for more details.')
        raise
    else:
        cols = ['name', 'dimensions', 'measurements']
        formatters = {
            'name': lambda x: x['name'],
            'dimensions': lambda x: utils.format_dict(x['dimensions']),
            'measurements': lambda x: utils.format_dictlist(x['measurements']),
        }
        if isinstance(metric, list):
            # print the list
            utils.print_list(metric, cols, formatters=formatters, sortby=2)
        else:
            # add the dictionary to a list, so print_list works
            metric_list = list()
            metric_list.append(metric)
            utils.print_list(
                metric_list,
                cols,
                formatters=formatters,
                sortby=2)


@utils.arg('name', metavar='<NOTIFICATION_NAME>',
           help='Name of the notification to create.')
@utils.arg('type', metavar='<EMAIL | SMS>',
           help='The notification type.  Types is one of [EMAIL, SMS].')
@utils.arg('address', metavar='<ADDRESS>',
           help='Depending on the type, a valid EMAIL or SMS Address')
def do_notification_create(mc, args):
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
        notification = mc.notifications.create(args, **fields)
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


@utils.arg('id', metavar='<NOTIFICATION_ID>',
           help='The ID of the notification. If not specified returns all.')
def do_notification_show(mc, args):
    '''Describe the notification.'''
    fields = {}
    fields['notification_id'] = args.id
    try:
        notification = mc.notifications.get(args, **fields)
    except exc.HTTPInternalServerError as e1:
        raise exc.CommandError('HTTPInternalServerError %s' % e1.code)
    except exc.BadRequest as e2:
        raise exc.CommandError('BadRequest %s' % e2.code)
    except exc.Unauthorized as e3:
        raise exc.CommandError('Unauthorized %s' % e3.code)
    except exc.HTTPNotFound as e4:
        raise exc.CommandError('Not Found %s' % e4.code)
    except Exception:
        print('Command Failed. Please use the -d option for more details.')
        raise
    else:
        formatters = {
            'name': utils.json_formatter,
            'id': utils.json_formatter,
            'type': utils.json_formatter,
            'address': utils.json_formatter,
            'links': utils.format_dictlist,
        }
        utils.print_dict(notification, formatters=formatters)
        #print notification


def do_notification_list(mc, args):
    '''List notifications for this tenant.'''
    try:
        notification = mc.notifications.list(args)
    except exc.HTTPInternalServerError as e1:
        raise exc.CommandError('HTTPInternalServerError %s' % e1.code)
    except exc.BadRequest as e2:
        raise exc.CommandError('BadRequest %s' % e2.code)
    except exc.Unauthorized as e3:
        raise exc.CommandError('Unauthorized %s' % e3.code)
    except exc.HTTPNotFound as e4:
        raise exc.CommandError('Not Found %s' % e4.code)
    except Exception:
        print('Command Failed. Please use the -d option for more details.')
        raise
    else:
        cols = ['name', 'id', 'type', 'address']
        formatters = {
            'name': lambda x: x['name'],
            'id': lambda x: x['id'],
            'type': lambda x: x['type'],
            'address': lambda x: x['address'],
        }
        if isinstance(notification, list):

            utils.print_list(
                notification,
                cols,
                formatters=formatters,
                sortby=0)
        else:
            notif_list = list()
            notif_list.append(notification)
            utils.print_list(notif_list, cols, formatters=formatters, sortby=0)


@utils.arg('id', metavar='<NOTIFICATION_ID>',
           help='The ID of the notification.')
def do_notification_delete(mc, args):
    '''Delete notification.'''
    fields = {}
    fields['notification_id'] = args.id
    try:
        notification = mc.notifications.delete(args, **fields)
    except exc.HTTPInternalServerError as e1:
        raise exc.CommandError('HTTPInternalServerError %s' % e1.code)
    except exc.Unauthorized as e3:
        raise exc.CommandError('Unauthorized %s' % e3.code)
    except exc.HTTPNotFound as e4:
        raise exc.CommandError('Not Found %s' % e4.code)
    except Exception:
        print('Command Failed. Please use the -d option for more details.')
        raise
    else:
        print('Successfully deleted notification')


@utils.arg('name', metavar='<ALARM_NAME>',
           help='Name of the alarm to create.')
@utils.arg('--description', metavar='<DESCRIPTION>',
           help='Description of the alarm.')
@utils.arg('expression', metavar='<EXPRESSION>',
           help='The alarm expression to evaluate. No spaces.')
@utils.arg('--alarm-actions', metavar='<NOTIFICATION-ID>',
           help='The notification method to use when an alarm state is ALARM. '
           'This param may be specified multiple times.',
           action='append')
@utils.arg('--ok-actions', metavar='<NOTIFICATION-ID>',
           help='The notification method to use when an alarm state is OK. '
           'This param may be specified multiple times.',
           action='append')
@utils.arg('--undetermined-actions', metavar='<NOTIFICATION-ID>',
           help='The notification method to use when an alarm state is '
           'UNDETERMINED. This param may be specified multiple times.',
           action='append')
def do_alarm_create(mc, args):
    '''Create alarm.'''
    fields = {}
    fields['name'] = args.name
    if args.description:
        fields['description'] = args.description
    fields['expression'] = args.expression
    if args.alarm_actions:
        fields['alarm_actions'] = args.alarm_actions
    if args.ok_actions:
        fields['ok_actions'] = args.ok_actions
    if args.undetermined_actions:
        fields['undetermined_actions'] = args.undetermined_actions
    try:
        alarm = mc.alarms.create(args, **fields)
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
        print(jsonutils.dumps(alarm, indent=2))


@utils.arg('id', metavar='<ALARM_ID>',
           help='The ID of the alarm.')
def do_alarm_show(mc, args):
    '''Describe the alarm.'''
    fields = {}
    fields['alarm_id'] = args.id
    try:
        alarm = mc.alarms.get(args, **fields)
    except exc.HTTPInternalServerError as e1:
        raise exc.CommandError('HTTPInternalServerError %s' % e1.code)
    except exc.BadRequest as e2:
        raise exc.CommandError('BadRequest %s' % e2.code)
    except exc.Unauthorized as e3:
        raise exc.CommandError('Unauthorized %s' % e3.code)
    except exc.HTTPNotFound as e4:
        raise exc.CommandError('Not Found %s' % e4.code)
    except Exception:
        print('Command Failed. Please use the -d option for more details.')
        raise
    else:
        # print out detail of a single alarm
        formatters = {
            'name': utils.json_formatter,
            'id': utils.json_formatter,
            'expression': utils.json_formatter,
            'state': utils.json_formatter,
            'enabled': utils.json_formatter,
            'alarm_actions': utils.json_formatter,
            'ok_actions': utils.json_formatter,
            'undetermined_actions': utils.json_formatter,
            'description': utils.json_formatter,
            'links': utils.format_dictlist,
        }
        utils.print_dict(alarm, formatters=formatters)
        #print alarm


def do_alarm_list(mc, args):
    '''List alarms for this tenant.'''
    try:
        alarm = mc.alarms.list(args)
    except exc.HTTPInternalServerError as e1:
        raise exc.CommandError('HTTPInternalServerError %s' % e1.code)
    except exc.BadRequest as e2:
        raise exc.CommandError('BadRequest %s' % e2.code)
    except exc.Unauthorized as e3:
        raise exc.CommandError('Unauthorized %s' % e3.code)
    except exc.HTTPNotFound as e4:
        raise exc.CommandError('Not Found %s' % e4.code)
    except Exception:
        print('Command Failed. Please use the -d option for more details.')
        raise
    else:
        cols = ['name', 'id', 'expression', 'state', 'enabled']
        formatters = {
            'name': lambda x: x['name'],
            'id': lambda x: x['id'],
            'expression': lambda x: x['expression'],
            'state': lambda x: x['state'],
            'enabled': lambda x: x['enabled'],
        }
        if isinstance(alarm, list):
            # print the list
            utils.print_list(alarm, cols, formatters=formatters, sortby=1)
        else:
            # add the dictionary to a list, so print_list works
            alarm_list = list()
            alarm_list.append(alarm)
            utils.print_list(alarm_list, cols, formatters=formatters, sortby=1)


@utils.arg('id', metavar='<ALARM_ID>',
           help='The ID of the alarm.')
def do_alarm_delete(mc, args):
    '''Delete alarm.'''
    fields = {}
    fields['alarm_id'] = args.id
    try:
        alarm = mc.alarms.delete(args, **fields)
    except exc.HTTPInternalServerError as e1:
        raise exc.CommandError('HTTPInternalServerError %s' % e1.code)
    except exc.Unauthorized as e3:
        raise exc.CommandError('Unauthorized %s' % e3.code)
    except exc.HTTPNotFound as e4:
        raise exc.CommandError('Not Found %s' % e4.code)
    except Exception:
        print('Command Failed. Please use the -d option for more details.')
        raise
    else:
        print('Successfully deleted alarm')
