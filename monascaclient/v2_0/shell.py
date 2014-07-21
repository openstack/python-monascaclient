# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
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

import json
from monascaclient.common import utils
import monascaclient.exc as exc
from monascaclient.openstack.common import jsonutils
import time


# Alarm valid types
severity_types = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
state_types = ['UNDETERMINED', 'ALARM', 'OK']
enabled_types = ['True', 'true', 'False', 'false']

# Notification valid types
notification_types = ['EMAIL', 'SMS']


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


@utils.arg('jsonbody', metavar='<JSON_BODY>',
           type=json.loads,
           help='The raw JSON body in single quotes. See api doc.')
def do_metric_create_raw(mc, args):
    '''Create metric from raw json body.'''
    fields = {}
    fields['jsonbody'] = args.jsonbody
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
        #meas_string = '{:10d}'.format(meas[0])
        meas_string = '{:20d}'.format(meas[0])
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


def format_statistic_timestamp(statistics, columns, name):
    # returns newline separated times for the timestamp column
    time_index = 0
    if statistics:
        time_index = columns.index(name)
    time_list = list()
    for timestamp in statistics:
        time_list.append(str(timestamp[time_index]))
    return '\n'.join(time_list)


def format_statistic_value(statistics, columns, stat_type):
    # find the index for column name
    stat_index = 0
    if statistics:
        stat_index = columns.index(stat_type)
    value_list = list()
    for stat in statistics:
        value_str = '{:12.2f}'.format(stat[stat_index])
        value_list.append(value_str)
    return '\n'.join(value_list)


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
            utils.print_list(metric, cols, formatters=formatters, sortby=3)
        else:
            # add the dictionary to a list, so print_list works
            metric_list = list()
            metric_list.append(metric)
            utils.print_list(
                metric_list,
                cols,
                formatters=formatters,
                sortby=3)


@utils.arg('name', metavar='<METRIC_NAME>',
           help='Name of the metric to report measurement statistics.')
@utils.arg('statistics', metavar='<STATISTICS>',
           help='Statistics is one or more (separated by commas) of '
           '[AVG, MIN, MAX, COUNT, SUM].')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to specify a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma.',
           action='append')
@utils.arg('starttime', metavar='<UTC_START_TIME>',
           help='measurements >= UTC time. format: 2014-01-01T00:00:00Z.')
@utils.arg('--endtime', metavar='<UTC_END_TIME>',
           help='measurements <= UTC time. format: 2014-01-01T00:00:00Z.')
@utils.arg('--period', metavar='<PERIOD>',
           help='number of seconds per interval (default is 300)')
def do_metric_statistics(mc, args):
    '''List measurement statistics for the specified metric.'''
    statistic_types = ['AVG', 'MIN', 'MAX', 'COUNT', 'SUM']
    statlist = args.statistics.split(',')
    for stat in statlist:
        if stat.upper() not in statistic_types:
            errmsg = 'Invalid type, not one of [' + \
                ', '.join(statistic_types) + ']'
            print(errmsg)
            return
    fields = {}
    fields['name'] = args.name
    if args.dimensions:
        fields['dimensions'] = utils.format_parameters(args.dimensions)
    fields['start_time'] = args.starttime
    if args.endtime:
        fields['end_time'] = args.endtime
    if args.period:
        fields['period'] = args.period
    fields['statistics'] = args.statistics
    try:
        metric = mc.metrics.list_statistics(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        if args.json:
            print(utils.json_formatter(metric))
            return
        cols = ['name', 'dimensions']
        # add dynamic column names
        if metric:
            column_names = metric[0]['columns']
            for name in column_names:
                cols.append(name)
        else:
            # when empty set, print_list needs a col
            cols.append('timestamp')

        formatters = {
            'name': lambda x: x['name'],
            'dimensions': lambda x: utils.format_dict(x['dimensions']),
            'timestamp': lambda x:
            format_statistic_timestamp(x['statistics'], x['columns'],
                                       'timestamp'),
            'avg': lambda x:
            format_statistic_value(x['statistics'], x['columns'], 'avg'),
            'min': lambda x:
            format_statistic_value(x['statistics'], x['columns'], 'min'),
            'max': lambda x:
            format_statistic_value(x['statistics'], x['columns'], 'max'),
            'count': lambda x:
            format_statistic_value(x['statistics'], x['columns'], 'count'),
            'sum': lambda x:
            format_statistic_value(x['statistics'], x['columns'], 'sum'),
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
    if args.type.upper() not in notification_types:
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
           help='Name of the notification.')
@utils.arg('type', metavar='<TYPE>',
           help='The notification type.  Type is one of [EMAIL, SMS].')
@utils.arg('address', metavar='<ADDRESS>',
           help='Depending on the type, a valid EMAIL or SMS Address')
def do_notification_update(mc, args):
    '''Update notification.'''
    fields = {}
    fields['notification_id'] = args.id
    fields['name'] = args.name
    if args.type.upper() not in notification_types:
        errmsg = 'Invalid type, not one of [' + \
                 ', '.join(state_types) + ']'
        print(errmsg)
        return
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
@utils.arg('--severity', metavar='<SEVERITY>',
           help='Severity is one of [LOW, MEDIUM, HIGH, CRITICAL].')
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
    fields['expression'] = utils.transform_expression(args.expression)
    if args.alarm_actions:
        fields['alarm_actions'] = args.alarm_actions
    if args.ok_actions:
        fields['ok_actions'] = args.ok_actions
    if args.undetermined_actions:
        fields['undetermined_actions'] = args.undetermined_actions
    if args.severity:
        if args.severity.upper() not in severity_types:
            errmsg = 'Invalid severity, not one of [' + \
                ', '.join(severity_types) + ']'
            print(errmsg)
            return
        fields['severity'] = args.severity
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
            'expression_data': utils.format_expression_data,
            'state': utils.json_formatter,
            'actions_enabled': utils.json_formatter,
            'alarm_actions': utils.json_formatter,
            'ok_actions': utils.json_formatter,
            'severity': utils.json_formatter,
            'undetermined_actions': utils.json_formatter,
            'description': utils.json_formatter,
            'links': utils.format_dictlist,
        }
        utils.print_dict(alarm, formatters=formatters)


@utils.arg('--name', metavar='<ALARM_NAME>',
           help='Name of the alarm.')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to specify a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma.',
           action='append')
@utils.arg('--state', metavar='<STATE>',
           help='STATE is one of [UNDETERMINED, OK, ALARM].')
def do_alarm_list(mc, args):
    '''List alarms for this tenant.'''
    fields = {}
    if args.name:
        fields['name'] = args.name
    if args.dimensions:
        quoted_dimstr = utils.transform_dim(','.join(args.dimensions))
        fields['dimensions'] = utils.format_parameters(quoted_dimstr.split(','))
    if args.state:
        if args.state.upper() not in state_types:
            errmsg = 'Invalid state, not one of [' + \
                ', '.join(state_types) + ']'
            print(errmsg)
            return
        fields['state'] = args.state
    try:
        alarm = mc.alarms.list(**fields)
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
           help='Name of the alarm.')
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
@utils.arg('actions_enabled', metavar='<ACTIONS-ENABLED>',
           help='The actions-enabled boolean is one of [true,false]')
@utils.arg('state', metavar='<STATE>',
           help='The alarm state. State is one of [UNDETERMINED,ALARM,OK]')
@utils.arg('--severity', metavar='<SEVERITY>',
           help='Severity is one of [LOW, MEDIUM, HIGH, CRITICAL].')
def do_alarm_update(mc, args):
    '''Update the alarm.'''
    fields = {}
    fields['alarm_id'] = args.id
    fields['name'] = args.name
    if args.description:
        fields['description'] = args.description
    fields['expression'] = utils.transform_expression(args.expression)
    if args.alarm_actions:
        fields['alarm_actions'] = args.alarm_actions
    if args.ok_actions:
        fields['ok_actions'] = args.ok_actions
    if args.undetermined_actions:
        fields['undetermined_actions'] = args.undetermined_actions
    if args.actions_enabled:
        if args.actions_enabled not in enabled_types:
            errmsg = 'Invalid value, not one of [' + \
                ', '.join(enabled_types) + ']'
            print(errmsg)
            return
        fields['actions_enabled'] = args.actions_enabled in ['true', 'True']
    if args.state:
        if args.state.upper() not in state_types:
            errmsg = 'Invalid state, not one of [' + \
                ', '.join(state_types) + ']'
            print(errmsg)
            return
        fields['state'] = args.state
    if args.severity:
        if args.severity.upper() not in severity_types:
            errmsg = 'Invalid severity, not one of [' + \
                ', '.join(severity_types) + ']'
            print(errmsg)
            return
        fields['severity'] = args.severity
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
           help='Name of the alarm.')
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
@utils.arg('--actions-enabled', metavar='<ACTIONS-ENABLED>',
           help='The actions-enabled boolean is one of [true,false]')
@utils.arg('--state', metavar='<STATE>',
           help='The alarm state. State is one of [UNDETERMINED,ALARM,OK]')
@utils.arg('--severity', metavar='<SEVERITY>',
           help='Severity is one of [LOW, MEDIUM, HIGH, CRITICAL].')
def do_alarm_patch(mc, args):
    '''Patch the alarm.'''
    fields = {}
    fields['alarm_id'] = args.id
    if args.name:
        fields['name'] = args.name
    if args.description:
        fields['description'] = args.description
    if args.expression:
        fields['expression'] = utils.transform_expression(args.expression)
    if args.alarm_actions:
        fields['alarm_actions'] = args.alarm_actions
    if args.ok_actions:
        fields['ok_actions'] = args.ok_actions
    if args.undetermined_actions:
        fields['undetermined_actions'] = args.undetermined_actions
    if args.actions_enabled:
        if args.actions_enabled not in enabled_types:
            errmsg = 'Invalid value, not one of [' + \
                ', '.join(enabled_types) + ']'
            print(errmsg)
            return
        fields['actions_enabled'] = args.actions_enabled in ['true', 'True']
    if args.state:
        if args.state.upper() not in state_types:
            errmsg = 'Invalid state, not one of [' + \
                ', '.join(state_types) + ']'
            print(errmsg)
            return
        fields['state'] = args.state
    if args.severity:
        if args.severity.upper() not in severity_types:
            errmsg = 'Invalid severity, not one of [' + \
                ', '.join(severity_types) + ']'
            print(errmsg)
            return
        fields['severity'] = args.severity
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
    '''Alarm state history.'''
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
            utils.print_list(alarm, cols, formatters=formatters, sortby=3)
        else:
            # add the dictionary to a list, so print_list works
            alarm_list = list()
            alarm_list.append(alarm)
            utils.print_list(alarm_list, cols, formatters=formatters, sortby=3)


@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to specify a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma.',
           action='append')
@utils.arg('--starttime', metavar='<UTC_START_TIME>',
           help='measurements >= UTC time. format: 2014-01-01T00:00:00Z.')
@utils.arg('--endtime', metavar='<UTC_END_TIME>',
           help='measurements <= UTC time. format: 2014-01-01T00:00:00Z.')
def do_alarm_history_list(mc, args):
    '''List alarms state history.'''
    fields = {}
    if args.dimensions:
        quoted_dimstr = utils.transform_dim(','.join(args.dimensions))
        fields['dimensions'] = utils.format_parameters(quoted_dimstr.split(','))
    if args.starttime:
        fields['start_time'] = args.starttime
    if args.endtime:
        fields['end_time'] = args.endtime
    try:
        alarm = mc.alarms.history_list(**fields)
    except exc.HTTPException as he:
        raise exc.CommandError(
            'HTTPException code=%s message=%s' %
            (he.code, he.message))
    else:
        if args.json:
            print(utils.json_formatter(alarm))
            return
        cols = ['alarm_id', 'new_state', 'old_state', 'reason',
                'reason_data', 'timestamp']
        formatters = {
            'alarm_id': lambda x: x['alarm_id'],
            'old_state': lambda x: x['old_state'],
            'new_state': lambda x: x['new_state'],
            'reason': lambda x: x['reason'],
            'reason_data': lambda x: x['reason_data'],
            'timestamp': lambda x: x['timestamp'],
        }
        if isinstance(alarm, list):
            # print the list
            utils.print_list(alarm, cols, formatters=formatters, sortby=5)
        else:
            # add the dictionary to a list, so print_list works
            alarm_list = list()
            alarm_list.append(alarm)
            utils.print_list(alarm_list, cols, formatters=formatters, sortby=5)
