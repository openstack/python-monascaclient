# Copyright 2014 HP
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
@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to create a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma.',
           action='append')
@utils.arg('--time', metavar='<UNIX_TIMESTAMP>',
           default=time.time(), type=int,
           help='Metric timestamp. Default: current timestamp.')
@utils.arg('value', metavar='<METRIC_VALUE>',
           type=float,
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
        mc.metrics.create(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        print('Successfully created metric')


@utils.arg('--name', metavar='<METRIC_NAME>',
           help='Name of the metric to list.')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to specify a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma.',
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
        metric = mc.metrics.list(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        if args.json:
            print(utils.json_formatter(metric))
            return
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


def format_measure_id(measurements):
    # returns newline separated measurements id's for the id column
    meas_string_list = list()
    for meas in measurements:
        meas_string = '{:10d}'.format(meas[0])
        meas_string_list.append(meas_string)
    return '\n'.join(meas_string_list)


def format_measure_timestamp(measurements):
    # returns newline separated times for the timestamp column
    meas_string_list = list()
    for meas in measurements:
        meas_string_list.append(str(meas[1]))
    return '\n'.join(meas_string_list)


def format_measure_value(measurements):
    # reutrns newline separated values for the value column
    meas_string_list = list()
    for meas in measurements:
        meas_string = '{:12.2f}'.format(meas[2])
        meas_string_list.append(meas_string)
    return '\n'.join(meas_string_list)


@utils.arg('name', metavar='<METRIC_NAME>',
           help='Name of the metric to list measurements.')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to specify a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma.',
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
        metric = mc.metrics.list_measurements(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        if args.json:
            print(utils.json_formatter(metric))
            return
        cols = ['name', 'dimensions', 'measurement_id', 'timestamp', 'value']
        formatters = {
            'name': lambda x: x['name'],
            'dimensions': lambda x: utils.format_dict(x['dimensions']),
            'measurement_id': lambda x: format_measure_id(x['measurements']),
            'timestamp': lambda x: format_measure_timestamp(x['measurements']),
            'value': lambda x: format_measure_value(x['measurements']),
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
@utils.arg('type', metavar='<TYPE>',
           help='The notification type.  Type is one of [EMAIL, SMS].')
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
        notification = mc.notifications.create(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        print(jsonutils.dumps(notification, indent=2))


@utils.arg('id', metavar='<NOTIFICATION_ID>',
           help='The ID of the notification. If not specified returns all.')
def do_notification_show(mc, args):
    '''Describe the notification.'''
    fields = {}
    fields['notification_id'] = args.id
    try:
        notification = mc.notifications.get(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        if args.json:
            print(utils.json_formatter(notification))
            return
        formatters = {
            'name': utils.json_formatter,
            'id': utils.json_formatter,
            'type': utils.json_formatter,
            'address': utils.json_formatter,
            'links': utils.format_dictlist,
        }
        utils.print_dict(notification, formatters=formatters)


def do_notification_list(mc, args):
    '''List notifications for this tenant.'''
    try:
        notification = mc.notifications.list()
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        if args.json:
            print(utils.json_formatter(notification))
            return
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
        mc.notifications.delete(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        print('Successfully deleted notification')


@utils.arg('id', metavar='<NOTIFICATION_ID>',
           help='The ID of the notification.')
@utils.arg('name', metavar='<NOTIFICATION_NAME>',
           help='Name of the notification to create.')
@utils.arg('type', metavar='<TYPE>',
           help='The notification type.  Type is one of [EMAIL, SMS].')
@utils.arg('address', metavar='<ADDRESS>',
           help='Depending on the type, a valid EMAIL or SMS Address')
def do_notification_update(mc, args):
    '''Update notification.'''
    fields = {}
    fields['notification_id'] = args.id
    fields['name'] = args.name
    fields['type'] = args.type
    fields['address'] = args.address
    try:
        notification = mc.notifications.update(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        print(jsonutils.dumps(notification, indent=2))


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
        alarm = mc.alarms.create(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        print(jsonutils.dumps(alarm, indent=2))


@utils.arg('id', metavar='<ALARM_ID>',
           help='The ID of the alarm.')
def do_alarm_show(mc, args):
    '''Describe the alarm.'''
    fields = {}
    fields['alarm_id'] = args.id
    try:
        alarm = mc.alarms.get(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        if args.json:
            print(utils.json_formatter(alarm))
            return
        # print out detail of a single alarm
        formatters = {
            'name': utils.json_formatter,
            'id': utils.json_formatter,
            'expression': utils.json_formatter,
            'state': utils.json_formatter,
            'actions_enabled': utils.json_formatter,
            'alarm_actions': utils.json_formatter,
            'ok_actions': utils.json_formatter,
            'undetermined_actions': utils.json_formatter,
            'description': utils.json_formatter,
            'links': utils.format_dictlist,
        }
        utils.print_dict(alarm, formatters=formatters)


def do_alarm_list(mc, args):
    '''List alarms for this tenant.'''
    try:
        alarm = mc.alarms.list()
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        if args.json:
            print(utils.json_formatter(alarm))
            return
        cols = ['name', 'id', 'expression', 'state', 'actions_enabled']
        formatters = {
            'name': lambda x: x['name'],
            'id': lambda x: x['id'],
            'expression': lambda x: x['expression'],
            'state': lambda x: x['state'],
            'actions_enabled': lambda x: x['actions_enabled'],
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
        mc.alarms.delete(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        print('Successfully deleted alarm')


@utils.arg('id', metavar='<ALARM_ID>',
           help='The ID of the alarm.')
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
@utils.arg('enabled', metavar='<ACTIONS-ENABLED>',
           help='The actions_enabled boolean is one of [true,false]')
@utils.arg('state', metavar='<STATE>',
           help='The alarm state. State is one of [UNDETERMINED,ALARM,OK]')
def do_alarm_update(mc, args):
    '''Update the alarm.'''
    fields = {}
    fields['alarm_id'] = args.id
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
    fields['actions_enabled'] = args.enabled
    fields['state'] = args.state
    try:
        alarm = mc.alarms.update(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        print(jsonutils.dumps(alarm, indent=2))


@utils.arg('id', metavar='<ALARM_ID>',
           help='The ID of the alarm.')
@utils.arg('--name', metavar='<ALARM_NAME>',
           help='Name of the alarm to create.')
@utils.arg('--description', metavar='<DESCRIPTION>',
           help='Description of the alarm.')
@utils.arg('--expression', metavar='<EXPRESSION>',
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
@utils.arg('--enabled', metavar='<ACTIONS-ENABLED>',
           help='The actions_enabled boolean is one of [true,false]')
@utils.arg('--state', metavar='<STATE>',
           help='The alarm state. State is one of [UNDETERMINED,ALARM,OK]')
def do_alarm_patch(mc, args):
    '''Patch the alarm.'''
    fields = {}
    fields['alarm_id'] = args.id
    if args.name:
        fields['name'] = args.name
    if args.description:
        fields['description'] = args.description
    if args.expression:
        fields['expression'] = args.expression
    if args.alarm_actions:
        fields['alarm_actions'] = args.alarm_actions
    if args.ok_actions:
        fields['ok_actions'] = args.ok_actions
    if args.undetermined_actions:
        fields['undetermined_actions'] = args.undetermined_actions
    if args.enabled:
        fields['actions_enabled'] = args.enabled
    if args.state:
        fields['state'] = args.state
    try:
        alarm = mc.alarms.patch(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        print(jsonutils.dumps(alarm, indent=2))


@utils.arg('id', metavar='<ALARM_ID>',
           help='The ID of the alarm.')
def do_alarm_history(mc, args):
    '''List alarm state history.'''
    fields = {}
    fields['alarm_id'] = args.id
    try:
        alarm = mc.alarms.history(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        if args.json:
            print(utils.json_formatter(alarm))
            return
        cols = ['alarm_id', 'new_state', 'old_state', 'timestamp', 'reason',
                'reason_data']
        formatters = {
            'alarm_id': lambda x: x['alarm_id'],
            'old_state': lambda x: x['old_state'],
            'new_state': lambda x: x['new_state'],
            'timestamp': lambda x: x['timestamp'],
            'reason': lambda x: x['reason'],
            'reason_data': lambda x: x['reason_data'],
        }
        if isinstance(alarm, list):
            # print the list
            utils.print_list(alarm, cols, formatters=formatters, sortby=1)
        else:
            # add the dictionary to a list, so print_list works
            alarm_list = list()
            alarm_list.append(alarm)
            utils.print_list(alarm_list, cols, formatters=formatters, sortby=1)
