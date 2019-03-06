# (C) Copyright 2014-2017 Hewlett Packard Enterprise Development LP
# Copyright 2017 FUJITSU LIMITED
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

import datetime
import numbers
import time

from keystoneauth1 import exceptions as k_exc
from osc_lib import exceptions as osc_exc

from monascaclient.common import utils

from oslo_serialization import jsonutils

# Alarm valid types
severity_types = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
state_types = ['UNDETERMINED', 'ALARM', 'OK']
enabled_types = ['True', 'true', 'False', 'false']
group_by_types = ['alarm_definition_id', 'name', 'state', 'severity',
                  'link', 'lifecycle_state', 'metric_name',
                  'dimension_name', 'dimension_value']
allowed_notification_sort_by = {'id', 'name', 'type', 'address', 'created_at', 'updated_at'}
allowed_alarm_sort_by = {'alarm_id', 'alarm_definition_id',
                         'alarm_definition_name', 'state', 'severity',
                         'lifecycle_state', 'link',
                         'state_updated_timestamp', 'updated_timestamp',
                         'created_timestamp'}
allowed_definition_sort_by = {'id', 'name', 'severity', 'updated_at', 'created_at'}

# Notification valid types
notification_types = ['EMAIL', 'WEBHOOK', 'PAGERDUTY']


@utils.arg('name', metavar='<METRIC_NAME>',
           help='Name of the metric to create.')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to create a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma. '
           'Dimensions need quoting when they contain special chars [&,(,),{,},>,<] '
           'that confuse the CLI parser.',
           action='append')
@utils.arg('--value-meta', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair for extra information about a value. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma. '
           'value_meta need quoting when they contain special chars [&,(,),{,},>,<] '
           'that confuse the CLI parser.',
           action='append')
@utils.arg('--time', metavar='<UNIX_TIMESTAMP>',
           default=time.time() * 1000, type=int,
           help='Metric timestamp in milliseconds. Default: current timestamp.')
@utils.arg('--project-id', metavar='<CROSS_PROJECT_ID>',
           help='The Project ID to create metric on behalf of. '
           'Requires monitoring-delegate role in keystone.')
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
    if args.value_meta:
        fields['value_meta'] = utils.format_parameters(args.value_meta)
    if args.project_id:
        fields['tenant_id'] = args.project_id
    try:
        mc.metrics.create(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print('Successfully created metric')


@utils.arg('jsonbody', metavar='<JSON_BODY>',
           type=jsonutils.loads,
           help='The raw JSON body in single quotes. See api doc.')
def do_metric_create_raw(mc, args):
    '''Create metric from raw json body.'''
    try:
        mc.metrics.create(**args.jsonbody)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print('Successfully created metric')


@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to specify a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma. '
           'Dimensions need quoting when they contain special chars [&,(,),{,},>,<] '
           'that confuse the CLI parser.',
           action='append')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum limit.')
@utils.arg('--tenant-id', metavar='<TENANT_ID>',
           help="Retrieve data for the specified tenant/project id instead of "
                "the tenant/project from the user's Keystone credentials.")
def do_metric_name_list(mc, args):
    '''List names of metrics.'''
    fields = {}
    if args.dimensions:
        fields['dimensions'] = utils.format_dimensions_query(args.dimensions)
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    if args.tenant_id:
        fields['tenant_id'] = args.tenant_id

    try:
        metric_names = mc.metrics.list_names(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        if args.json:
            print(utils.json_formatter(metric_names))
            return
        if isinstance(metric_names, list):
            utils.print_list(metric_names, ['Name'], formatters={'Name': lambda x: x['name']})


@utils.arg('--name', metavar='<METRIC_NAME>',
           help='Name of the metric to list.')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to specify a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma. '
           'Dimensions need quoting when they contain special chars [&,(,),{,},>,<] '
           'that confuse the CLI parser.',
           action='append')
@utils.arg('--starttime', metavar='<UTC_START_TIME>',
           help='measurements >= UTC time. format: 2014-01-01T00:00:00Z. OR'
                ' Format: -120 (previous 120 minutes).')
@utils.arg('--endtime', metavar='<UTC_END_TIME>',
           help='measurements <= UTC time. format: 2014-01-01T00:00:00Z.')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum limit.')
@utils.arg('--tenant-id', metavar='<TENANT_ID>',
           help="Retrieve data for the specified tenant/project id instead of "
                "the tenant/project from the user's Keystone credentials.")
def do_metric_list(mc, args):
    '''List metrics for this tenant.'''
    fields = {}
    if args.name:
        fields['name'] = args.name
    if args.dimensions:
        fields['dimensions'] = utils.format_dimensions_query(args.dimensions)
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    if args.starttime:
        _translate_starttime(args)
        fields['start_time'] = args.starttime
    if args.endtime:
        fields['end_time'] = args.endtime
    if args.tenant_id:
        fields['tenant_id'] = args.tenant_id

    try:
        metric = mc.metrics.list(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
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
            utils.print_list(metric, cols, formatters=formatters)
        else:
            # add the dictionary to a list, so print_list works
            metric_list = list()
            metric_list.append(metric)
            utils.print_list(
                metric_list,
                cols,
                formatters=formatters)


@utils.arg('--metric-name', metavar='<METRIC_NAME>',
           help='Name of the metric to report dimension name list.',
           action='append')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum '
                'limit.')
@utils.arg('--tenant-id', metavar='<TENANT_ID>',
           help="Retrieve data for the specified tenant/project id instead of "
                "the tenant/project from the user's Keystone credentials.")
def do_dimension_name_list(mc, args):
    '''List names of metric dimensions.'''
    fields = {}
    if args.metric_name:
        fields['metric_name'] = args.metric_name
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    if args.tenant_id:
        fields['tenant_id'] = args.tenant_id

    try:
        dimension_names = mc.metrics.list_dimension_names(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))

    if args.json:
        print(utils.json_formatter(dimension_names))
        return

    if isinstance(dimension_names, list):
        utils.print_list(dimension_names, ['Dimension Names'], formatters={
            'Dimension Names': lambda x: x['dimension_name']})


@utils.arg('dimension_name', metavar='<DIMENSION_NAME>',
           help='Name of the dimension to list dimension values.')
@utils.arg('--metric-name', metavar='<METRIC_NAME>',
           help='Name of the metric to report dimension value list.',
           action='append')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum '
                'limit.')
@utils.arg('--tenant-id', metavar='<TENANT_ID>',
           help="Retrieve data for the specified tenant/project id instead of "
                "the tenant/project from the user's Keystone credentials.")
def do_dimension_value_list(mc, args):
    '''List names of metric dimensions.'''
    fields = {}
    fields['dimension_name'] = args.dimension_name
    if args.metric_name:
        fields['metric_name'] = args.metric_name
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    if args.tenant_id:
        fields['tenant_id'] = args.tenant_id

    try:
        dimension_values = mc.metrics.list_dimension_values(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))

    if args.json:
        print(utils.json_formatter(dimension_values))
        return

    if isinstance(dimension_values, list):
        utils.print_list(dimension_values, ['Dimension Values'], formatters={
            'Dimension Values': lambda x: x['dimension_value']})


def format_measure_timestamp(measurements):
    # returns newline separated times for the timestamp column
    return '\n'.join([str(m[0]) for m in measurements])


def format_measure_value(measurements):
    # returns newline separated values for the value column
    return '\n'.join(['{:12.3f}'.format(m[1]) for m in measurements])


def format_value_meta(measurements):
    # returns newline separated values for the value column
    measure_string_list = list()
    for measure in measurements:
        if len(measure) < 3:
            measure_string = ""
        else:
            meta_string_list = []
            for k, v in measure[2].items():
                if isinstance(v, numbers.Number):
                    m_str = k + ': ' + str(v)
                else:
                    m_str = k + ': ' + v
                meta_string_list.append(m_str)
            measure_string = ','.join(meta_string_list)
        measure_string_list.append(measure_string)
    return '\n'.join(measure_string_list)


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
        value_str = '{:12.3f}'.format(stat[stat_index])
        value_list.append(value_str)
    return '\n'.join(value_list)


def format_metric_name(metrics):
    # returns newline separated metric names for the column
    metric_string_list = list()
    for metric in metrics:
        metric_name = metric['name']
        metric_dimensions = metric['dimensions']
        metric_string_list.append(metric_name)
        # need to line up with dimensions column
        rng = len(metric_dimensions)
        for i in range(rng):
            if i == rng - 1:
                # last one
                break
            metric_string_list.append(" ")
    return '\n'.join(metric_string_list)


def format_metric_dimensions(metrics):
    # returns newline separated dimension key values for the column
    metric_string_list = list()
    for metric in metrics:
        metric_dimensions = metric['dimensions']
        for k, v in metric_dimensions.items():
            if isinstance(v, numbers.Number):
                d_str = k + ': ' + str(v)
            else:
                d_str = k + ': ' + v
            metric_string_list.append(d_str)
    return '\n'.join(metric_string_list)


@utils.arg('name', metavar='<METRIC_NAME>',
           help='Name of the metric to list measurements.')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to specify a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma. '
           'Dimensions need quoting when they contain special chars [&,(,),{,},>,<] '
           'that confuse the CLI parser.',
           action='append')
@utils.arg('starttime', metavar='<UTC_START_TIME>',
           help='measurements >= UTC time. format: 2014-01-01T00:00:00Z.'
                ' OR Format: -120 (previous 120 minutes).')
@utils.arg('--endtime', metavar='<UTC_END_TIME>',
           help='measurements <= UTC time. format: 2014-01-01T00:00:00Z.')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum limit.')
@utils.arg('--merge_metrics', action='store_const',
           const=True,
           help='Merge multiple metrics into a single result.')
@utils.arg('--group_by', metavar='<KEY1,KEY2,...>',
           help='Select which keys to use for grouping. A \'*\' groups by all keys.')
@utils.arg('--tenant-id', metavar='<TENANT_ID>',
           help="Retrieve data for the specified tenant/project id instead of "
                "the tenant/project from the user's Keystone credentials.")
def do_measurement_list(mc, args):
    '''List measurements for the specified metric.'''
    fields = {}
    fields['name'] = args.name

    if args.dimensions:
        fields['dimensions'] = utils.format_dimensions_query(args.dimensions)
    _translate_starttime(args)
    fields['start_time'] = args.starttime
    if args.endtime:
        fields['end_time'] = args.endtime
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    if args.merge_metrics:
        fields['merge_metrics'] = args.merge_metrics
    if args.group_by:
        fields['group_by'] = args.group_by
    if args.tenant_id:
        fields['tenant_id'] = args.tenant_id

    try:
        metric = mc.metrics.list_measurements(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        if args.json:
            print(utils.json_formatter(metric))
            return
        cols = ['name', 'dimensions', 'timestamp', 'value', 'value_meta']
        formatters = {
            'name': lambda x: x['name'],
            'dimensions': lambda x: utils.format_dict(x['dimensions']),
            'timestamp': lambda x: format_measure_timestamp(x['measurements']),
            'value': lambda x: format_measure_value(x['measurements']),
            'value_meta': lambda x: format_value_meta(x['measurements']),
        }
        if isinstance(metric, list):
            # print the list
            utils.print_list(metric, cols, formatters=formatters)
        else:
            # add the dictionary to a list, so print_list works
            metric_list = list()
            metric_list.append(metric)
            utils.print_list(
                metric_list,
                cols,
                formatters=formatters)


@utils.arg('name', metavar='<METRIC_NAME>',
           help='Name of the metric to report measurement statistics.')
@utils.arg('statistics', metavar='<STATISTICS>',
           help='Statistics is one or more (separated by commas) of '
           '[AVG, MIN, MAX, COUNT, SUM].')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to specify a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma. '
           'Dimensions need quoting when they contain special chars [&,(,),{,},>,<] '
           'that confuse the CLI parser.',
           action='append')
@utils.arg('starttime', metavar='<UTC_START_TIME>',
           help='measurements >= UTC time. format: 2014-01-01T00:00:00Z. OR'
                ' Format: -120 (previous 120 minutes).')
@utils.arg('--endtime', metavar='<UTC_END_TIME>',
           help='measurements <= UTC time. format: 2014-01-01T00:00:00Z.')
@utils.arg('--period', metavar='<PERIOD>',
           help='number of seconds per interval (default is 300)')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum limit.')
@utils.arg('--merge_metrics', action='store_const',
           const=True,
           help='Merge multiple metrics into a single result.')
@utils.arg('--group_by', metavar='<KEY1,KEY2,...>',
           help='Select which keys to use for grouping. A \'*\' groups by all keys.')
@utils.arg('--tenant-id', metavar='<TENANT_ID>',
           help="Retrieve data for the specified tenant/project id instead of "
                "the tenant/project from the user's Keystone credentials.")
def do_metric_statistics(mc, args):
    '''List measurement statistics for the specified metric.'''
    statistic_types = ['AVG', 'MIN', 'MAX', 'COUNT', 'SUM']
    statlist = args.statistics.split(',')
    for stat in statlist:
        if stat.upper() not in statistic_types:
            errmsg = ('Invalid type, not one of [' +
                      ', '.join(statistic_types) + ']')
            raise osc_exc.CommandError(errmsg)

    fields = {}
    fields['name'] = args.name
    if args.dimensions:
        fields['dimensions'] = utils.format_dimensions_query(args.dimensions)
    _translate_starttime(args)
    fields['start_time'] = args.starttime
    if args.endtime:
        fields['end_time'] = args.endtime
    if args.period:
        fields['period'] = args.period
    fields['statistics'] = args.statistics
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    if args.merge_metrics:
        fields['merge_metrics'] = args.merge_metrics
    if args.group_by:
        fields['group_by'] = args.group_by
    if args.tenant_id:
        fields['tenant_id'] = args.tenant_id

    try:
        metric = mc.metrics.list_statistics(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
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
            utils.print_list(metric, cols, formatters=formatters)
        else:
            # add the dictionary to a list, so print_list works
            metric_list = list()
            metric_list.append(metric)
            utils.print_list(
                metric_list,
                cols,
                formatters=formatters)


def _validate_notification_period(period, notification_type):
    if notification_type != 'WEBHOOK' and period != 0:
        print("Invalid period, can only be non zero for webhooks")
        return False
    return True


@utils.arg('name', metavar='<NOTIFICATION_NAME>',
           help='Name of the notification to create.')
@utils.arg('type', metavar='<TYPE>',
           help='The notification type. Type must be EMAIL, WEBHOOK, or PAGERDUTY.')
@utils.arg('address', metavar='<ADDRESS>',
           help='A valid EMAIL Address, URL, or SERVICE KEY.')
@utils.arg('--period', metavar='<PERIOD>', type=int, default=0,
           help='A period for the notification method. Can only be non zero with webhooks')
def do_notification_create(mc, args):
    '''Create notification.'''

    fields = {}
    fields['name'] = args.name
    fields['type'] = args.type
    fields['address'] = args.address
    if args.period:
        if not _validate_notification_period(args.period, args.type.upper()):
            return
        fields['period'] = args.period
    try:
        notification = mc.notifications.create(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print(jsonutils.dumps(notification, indent=2))


@utils.arg('id', metavar='<NOTIFICATION_ID>',
           help='The ID of the notification.')
def do_notification_show(mc, args):
    '''Describe the notification.'''
    fields = {}
    fields['notification_id'] = args.id
    try:
        notification = mc.notifications.get(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        if args.json:
            print(utils.json_formatter(notification))
            return
        formatters = {
            'name': utils.json_formatter,
            'id': utils.json_formatter,
            'type': utils.json_formatter,
            'address': utils.json_formatter,
            'period': utils.json_formatter,
            'links': utils.format_dictlist,
        }
        utils.print_dict(notification, formatters=formatters)


@utils.arg('--sort-by', metavar='<SORT BY FIELDS>',
           help='Fields to sort by as a comma separated list. Valid values are id, '
                'name, type, address, created_at, updated_at. '
                'Fields may be followed by "asc" or "desc", ex "address desc", '
                'to set the direction of sorting.')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum limit.')
def do_notification_list(mc, args):
    '''List notifications for this tenant.'''
    fields = {}
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    if args.sort_by:
        sort_by = args.sort_by.split(',')
        for field in sort_by:
            field_values = field.lower().split()
            if len(field_values) > 2:
                print("Invalid sort_by value {}".format(field))
            if field_values[0] not in allowed_notification_sort_by:
                print("Sort-by field name {} is not in [{}]".format(field_values[0],
                                                                    allowed_notification_sort_by))
                return
            if len(field_values) > 1 and field_values[1] not in ['asc', 'desc']:
                print("Invalid value {}, must be asc or desc".format(field_values[1]))
        fields['sort_by'] = args.sort_by

    try:
        notification = mc.notifications.list(**fields)
    except osc_exc.ClientException as he:
        raise osc_exc.CommandError(
            'ClientException code=%s message=%s' %
            (he.code, he.message))
    else:
        if args.json:
            print(utils.json_formatter(notification))
            return
        cols = ['name', 'id', 'type', 'address', 'period']
        formatters = {
            'name': lambda x: x['name'],
            'id': lambda x: x['id'],
            'type': lambda x: x['type'],
            'address': lambda x: x['address'],
            'period': lambda x: x['period'],
        }
        if isinstance(notification, list):

            utils.print_list(
                notification,
                cols,
                formatters=formatters)
        else:
            notif_list = list()
            notif_list.append(notification)
            utils.print_list(notif_list, cols, formatters=formatters)


@utils.arg('id', metavar='<NOTIFICATION_ID>',
           help='The ID of the notification.')
def do_notification_delete(mc, args):
    '''Delete notification.'''
    fields = {}
    fields['notification_id'] = args.id
    try:
        mc.notifications.delete(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print('Successfully deleted notification')


@utils.arg('id', metavar='<NOTIFICATION_ID>',
           help='The ID of the notification.')
@utils.arg('name', metavar='<NOTIFICATION_NAME>',
           help='Name of the notification.')
@utils.arg('type', metavar='<TYPE>',
           help='The notification type. Type must be either EMAIL, WEBHOOK, or PAGERDUTY.')
@utils.arg('address', metavar='<ADDRESS>',
           help='A valid EMAIL Address, URL, or SERVICE KEY.')
@utils.arg('period', metavar='<PERIOD>', type=int,
           help='A period for the notification method. Can only be non zero with webhooks')
def do_notification_update(mc, args):
    '''Update notification.'''
    fields = {}
    fields['notification_id'] = args.id
    fields['name'] = args.name

    fields['type'] = args.type
    fields['address'] = args.address
    if not _validate_notification_period(args.period, args.type.upper()):
        return
    fields['period'] = args.period
    try:
        notification = mc.notifications.update(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print(jsonutils.dumps(notification, indent=2))


@utils.arg('id', metavar='<NOTIFICATION_ID>',
           help='The ID of the notification.')
@utils.arg('--name', metavar='<NOTIFICATION_NAME>',
           help='Name of the notification.')
@utils.arg('--type', metavar='<TYPE>',
           help='The notification type. Type must be either EMAIL, WEBHOOK, or PAGERDUTY.')
@utils.arg('--address', metavar='<ADDRESS>',
           help='A valid EMAIL Address, URL, or SERVICE KEY.')
@utils.arg('--period', metavar='<PERIOD>', type=int,
           help='A period for the notification method. Can only be non zero with webhooks')
def do_notification_patch(mc, args):
    '''Patch notification.'''
    fields = {}
    fields['notification_id'] = args.id
    if args.name:
        fields['name'] = args.name

    if args.type:
        fields['type'] = args.type
    if args.address:
        fields['address'] = args.address
    if args.period or args.period == 0:
        if args.type and not _validate_notification_period(
                args.period, args.type.upper()):
            return
        fields['period'] = args.period
    try:
        notification = mc.notifications.patch(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print(jsonutils.dumps(notification, indent=2))


def _validate_severity(severity):
    if severity.upper() not in severity_types:
        errmsg = ('Invalid severity, not one of [' +
                  ', '.join(severity_types) + ']')
        print(errmsg)
        return False
    return True


@utils.arg('name', metavar='<ALARM_DEFINITION_NAME>',
           help='Name of the alarm definition to create.')
@utils.arg('--description', metavar='<DESCRIPTION>',
           help='Description of the alarm.')
@utils.arg('expression', metavar='<EXPRESSION>',
           help='The alarm expression to evaluate. Quoted.')
@utils.arg('--severity', metavar='<SEVERITY>',
           help='Severity is one of [LOW, MEDIUM, HIGH, CRITICAL].')
@utils.arg('--match-by', metavar='<MATCH_BY_DIMENSION_KEY1,MATCH_BY_DIMENSION_KEY2,'
                                 '...>',
           help='The metric dimensions to use to create unique alarms. '
           'One or more dimension key names separated by a comma. '
           'Key names need quoting when they contain special chars [&,(,),{,},>,<] '
           'that confuse the CLI parser.')
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
def do_alarm_definition_create(mc, args):
    '''Create an alarm definition.'''
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
    if args.severity:
        if not _validate_severity(args.severity):
            return
        fields['severity'] = args.severity
    if args.match_by:
        fields['match_by'] = args.match_by.split(',')
    try:
        alarm = mc.alarm_definitions.create(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print(jsonutils.dumps(alarm, indent=2))


@utils.arg('id', metavar='<ALARM_DEFINITION_ID>',
           help='The ID of the alarm definition.')
def do_alarm_definition_show(mc, args):
    '''Describe the alarm definition.'''
    fields = {}
    fields['alarm_id'] = args.id
    try:
        alarm = mc.alarm_definitions.get(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
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
            'match_by': utils.json_formatter,
            'actions_enabled': utils.json_formatter,
            'alarm_actions': utils.json_formatter,
            'ok_actions': utils.json_formatter,
            'severity': utils.json_formatter,
            'undetermined_actions': utils.json_formatter,
            'description': utils.json_formatter,
            'links': utils.format_dictlist,
        }
        utils.print_dict(alarm, formatters=formatters)


@utils.arg('--name', metavar='<ALARM_DEFINITION_NAME>',
           help='Name of the alarm definition.')
@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to specify a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma. '
           'Dimensions need quoting when they contain special chars [&,(,),{,},>,<] '
           'that confuse the CLI parser.',
           action='append')
@utils.arg('--severity', metavar='<SEVERITY>',
           help='Severity is one of ["LOW", "MEDIUM", "HIGH", "CRITICAL"].')
@utils.arg('--sort-by', metavar='<SORT BY FIELDS>',
           help='Fields to sort by as a comma separated list. Valid values are id, '
                'name, severity, created_at, updated_at. '
                'Fields may be followed by "asc" or "desc", ex "severity desc", '
                'to set the direction of sorting.')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum limit.')
def do_alarm_definition_list(mc, args):
    '''List alarm definitions for this tenant.'''
    fields = {}
    if args.name:
        fields['name'] = args.name
    if args.dimensions:
        fields['dimensions'] = utils.format_dimensions_query(args.dimensions)
    if args.severity:
        if not _validate_severity(args.severity):
            return
        fields['severity'] = args.severity
    if args.sort_by:
        sort_by = args.sort_by.split(',')
        for field in sort_by:
            field_values = field.split()
            if len(field_values) > 2:
                print("Invalid sort_by value {}".format(field))
            if field_values[0] not in allowed_definition_sort_by:
                print("Sort-by field name {} is not in [{}]".format(field_values[0],
                                                                    allowed_definition_sort_by))
                return
            if len(field_values) > 1 and field_values[1] not in ['asc', 'desc']:
                print("Invalid value {}, must be asc or desc".format(field_values[1]))
        fields['sort_by'] = args.sort_by
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    try:
        alarm = mc.alarm_definitions.list(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        if args.json:
            print(utils.json_formatter(alarm))
            return
        cols = ['name', 'id', 'expression', 'match_by', 'actions_enabled']
        formatters = {
            'name': lambda x: x['name'],
            'id': lambda x: x['id'],
            'expression': lambda x: x['expression'],
            'match_by': lambda x: utils.format_list(x['match_by']),
            'actions_enabled': lambda x: x['actions_enabled'],
        }
        if isinstance(alarm, list):
            # print the list
            utils.print_list(alarm, cols, formatters=formatters)
        else:
            # add the dictionary to a list, so print_list works
            alarm_list = list()
            alarm_list.append(alarm)
            utils.print_list(alarm_list, cols, formatters=formatters)


@utils.arg('id', metavar='<ALARM_DEFINITION_ID>',
           help='The ID of the alarm definition.')
def do_alarm_definition_delete(mc, args):
    '''Delete the alarm definition.'''
    fields = {}
    fields['alarm_id'] = args.id
    try:
        mc.alarm_definitions.delete(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print('Successfully deleted alarm definition')


@utils.arg('id', metavar='<ALARM_DEFINITION_ID>',
           help='The ID of the alarm definition.')
@utils.arg('name', metavar='<ALARM_DEFINITION_NAME>',
           help='Name of the alarm definition.')
@utils.arg('description', metavar='<DESCRIPTION>',
           help='Description of the alarm.')
@utils.arg('expression', metavar='<EXPRESSION>',
           help='The alarm expression to evaluate. Quoted.')
@utils.arg('alarm_actions', metavar='<ALARM-NOTIFICATION-ID1,ALARM-NOTIFICATION-ID2,...>',
           help='The notification method(s) to use when an alarm state is ALARM '
                'as a comma separated list.')
@utils.arg('ok_actions', metavar='<OK-NOTIFICATION-ID1,OK-NOTIFICATION-ID2,...>',
           help='The notification method(s) to use when an alarm state is OK '
           'as a comma separated list.')
@utils.arg('undetermined_actions',
           metavar='<UNDETERMINED-NOTIFICATION-ID1,UNDETERMINED-NOTIFICATION-ID2,...>',
           help='The notification method(s) to use when an alarm state is UNDETERMINED '
                'as a comma separated list.')
@utils.arg('actions_enabled', metavar='<ACTIONS-ENABLED>',
           help='The actions-enabled boolean is one of [true,false]')
@utils.arg('match_by', metavar='<MATCH_BY_DIMENSION_KEY1,MATCH_BY_DIMENSION_KEY2,...>',
           help='The metric dimensions to use to create unique alarms. '
           'One or more dimension key names separated by a comma. '
           'Key names need quoting when they contain special chars [&,(,),{,},>,<] '
           'that confuse the CLI parser.')
@utils.arg('severity', metavar='<SEVERITY>',
           help='Severity is one of [LOW, MEDIUM, HIGH, CRITICAL].')
def do_alarm_definition_update(mc, args):
    '''Update the alarm definition.'''
    fields = {}
    fields['alarm_id'] = args.id
    fields['name'] = args.name
    fields['description'] = args.description
    fields['expression'] = args.expression
    fields['alarm_actions'] = _arg_split_patch_update(args.alarm_actions)
    fields['ok_actions'] = _arg_split_patch_update(args.ok_actions)
    fields['undetermined_actions'] = _arg_split_patch_update(args.undetermined_actions)
    if args.actions_enabled not in enabled_types:
        errmsg = ('Invalid value, not one of [' +
                  ', '.join(enabled_types) + ']')
        print(errmsg)
        return
    fields['actions_enabled'] = args.actions_enabled in ['true', 'True']
    fields['match_by'] = _arg_split_patch_update(args.match_by)
    if not _validate_severity(args.severity):
        return
    fields['severity'] = args.severity
    try:
        alarm = mc.alarm_definitions.update(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print(jsonutils.dumps(alarm, indent=2))


@utils.arg('id', metavar='<ALARM_DEFINITION_ID>',
           help='The ID of the alarm definition.')
@utils.arg('--name', metavar='<ALARM_DEFINITION_NAME>',
           help='Name of the alarm definition.')
@utils.arg('--description', metavar='<DESCRIPTION>',
           help='Description of the alarm.')
@utils.arg('--expression', metavar='<EXPRESSION>',
           help='The alarm expression to evaluate. Quoted.')
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
           help='The actions-enabled boolean is one of [true,false].')
@utils.arg('--severity', metavar='<SEVERITY>',
           help='Severity is one of [LOW, MEDIUM, HIGH, CRITICAL].')
def do_alarm_definition_patch(mc, args):
    '''Patch the alarm definition.'''
    fields = {}
    fields['alarm_id'] = args.id
    if args.name:
        fields['name'] = args.name
    if args.description:
        fields['description'] = args.description
    if args.expression:
        fields['expression'] = args.expression
    if args.alarm_actions:
        fields['alarm_actions'] = _arg_split_patch_update(args.alarm_actions, patch=True)
    if args.ok_actions:
        fields['ok_actions'] = _arg_split_patch_update(args.ok_actions, patch=True)
    if args.undetermined_actions:
        fields['undetermined_actions'] = _arg_split_patch_update(args.undetermined_actions,
                                                                 patch=True)
    if args.actions_enabled:
        if args.actions_enabled not in enabled_types:
            errmsg = ('Invalid value, not one of [' +
                      ', '.join(enabled_types) + ']')
            print(errmsg)
            return
        fields['actions_enabled'] = args.actions_enabled in ['true', 'True']
    if args.severity:
        if not _validate_severity(args.severity):
            return
        fields['severity'] = args.severity
    try:
        alarm = mc.alarm_definitions.patch(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print(jsonutils.dumps(alarm, indent=2))


@utils.arg('--alarm-definition-id', metavar='<ALARM_DEFINITION_ID>',
           help='The ID of the alarm definition.')
@utils.arg('--metric-name', metavar='<METRIC_NAME>',
           help='Name of the metric.')
@utils.arg('--metric-dimensions', metavar='<KEY1=VALUE1,KEY2,KEY3=VALUE2...>',
           help='key value pair used to specify a metric dimension or '
                'just key to select all values of that dimension.'
                'This can be specified multiple times, or once with parameters '
                'separated by a comma. '
                'Dimensions need quoting when they contain special chars [&,(,),{,},>,<] '
                'that confuse the CLI parser.',
           action='append')
@utils.arg('--state', metavar='<ALARM_STATE>',
           help='ALARM_STATE is one of [UNDETERMINED, OK, ALARM].')
@utils.arg('--severity', metavar='<SEVERITY>',
           help='Severity is one of ["LOW", "MEDIUM", "HIGH", "CRITICAL"].')
@utils.arg('--state-updated-start-time', metavar='<UTC_STATE_UPDATED_START>',
           help='Return all alarms whose state was updated on or after the time specified.')
@utils.arg('--lifecycle-state', metavar='<LIFECYCLE_STATE>',
           help='The lifecycle state of the alarm.')
@utils.arg('--link', metavar='<LINK>',
           help='The link to external data associated with the alarm.')
@utils.arg('--sort-by', metavar='<SORT BY FIELDS>',
           help='Fields to sort by as a comma separated list. Valid values are alarm_id, '
                'alarm_definition_id, state, severity, lifecycle_state, link, '
                'state_updated_timestamp, updated_timestamp, created_timestamp. '
                'Fields may be followed by "asc" or "desc", ex "severity desc", '
                'to set the direction of sorting.')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum limit.')
def do_alarm_list(mc, args):
    '''List alarms for this tenant.'''
    fields = {}
    if args.alarm_definition_id:
        fields['alarm_definition_id'] = args.alarm_definition_id
    if args.metric_name:
        fields['metric_name'] = args.metric_name
    if args.metric_dimensions:
        fields['metric_dimensions'] = utils.format_dimensions_query(args.metric_dimensions)
    if args.state:
        if args.state.upper() not in state_types:
            errmsg = ('Invalid state, not one of [' +
                      ', '.join(state_types) + ']')
            print(errmsg)
            return
        fields['state'] = args.state
    if args.severity:
        if not _validate_severity(args.severity):
            return
        fields['severity'] = args.severity
    if args.state_updated_start_time:
        fields['state_updated_start_time'] = args.state_updated_start_time
    if args.lifecycle_state:
        fields['lifecycle_state'] = args.lifecycle_state
    if args.link:
        fields['link'] = args.link
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    if args.sort_by:
        sort_by = args.sort_by.split(',')
        for field in sort_by:
            field_values = field.lower().split()
            if len(field_values) > 2:
                print("Invalid sort_by value {}".format(field))
            if field_values[0] not in allowed_alarm_sort_by:
                print("Sort-by field name {} is not in [{}]".format(field_values[0],
                                                                    allowed_alarm_sort_by))
                return
            if len(field_values) > 1 and field_values[1] not in ['asc', 'desc']:
                print("Invalid value {}, must be asc or desc".format(field_values[1]))
        fields['sort_by'] = args.sort_by
    try:
        alarm = mc.alarms.list(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        if args.json:
            print(utils.json_formatter(alarm))
            return
        cols = ['id', 'alarm_definition_id', 'alarm_definition_name', 'metric_name',
                'metric_dimensions', 'severity', 'state', 'lifecycle_state', 'link',
                'state_updated_timestamp', 'updated_timestamp', "created_timestamp"]
        formatters = {
            'id': lambda x: x['id'],
            'alarm_definition_id': lambda x: x['alarm_definition']['id'],
            'alarm_definition_name': lambda x: x['alarm_definition']['name'],
            'metric_name': lambda x: format_metric_name(x['metrics']),
            'metric_dimensions': lambda x: format_metric_dimensions(x['metrics']),
            'severity': lambda x: x['alarm_definition']['severity'],
            'state': lambda x: x['state'],
            'lifecycle_state': lambda x: x['lifecycle_state'],
            'link': lambda x: x['link'],
            'state_updated_timestamp': lambda x: x['state_updated_timestamp'],
            'updated_timestamp': lambda x: x['updated_timestamp'],
            'created_timestamp': lambda x: x['created_timestamp'],
        }
        if isinstance(alarm, list):
            # print the list
            utils.print_list(alarm, cols, formatters=formatters)
        else:
            # add the dictionary to a list, so print_list works
            alarm_list = list()
            alarm_list.append(alarm)
            utils.print_list(alarm_list, cols, formatters=formatters)


@utils.arg('id', metavar='<ALARM_ID>',
           help='The ID of the alarm.')
def do_alarm_show(mc, args):
    '''Describe the alarm.'''
    fields = {}
    fields['alarm_id'] = args.id
    try:
        alarm = mc.alarms.get(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        if args.json:
            print(utils.json_formatter(alarm))
            return
        # print out detail of a single alarm
        formatters = {
            'id': utils.json_formatter,
            'alarm_definition': utils.json_formatter,
            'metrics': utils.json_formatter,
            'state': utils.json_formatter,
            'links': utils.format_dictlist,
        }
        utils.print_dict(alarm, formatters=formatters)


@utils.arg('id', metavar='<ALARM_ID>',
           help='The ID of the alarm.')
@utils.arg('state', metavar='<ALARM_STATE>',
           help='ALARM_STATE is one of [UNDETERMINED, OK, ALARM].')
@utils.arg('lifecycle_state', metavar='<LIFECYCLE_STATE>',
           help='The lifecycle state of the alarm.')
@utils.arg('link', metavar='<LINK>',
           help='A link to an external resource with information about the alarm.')
def do_alarm_update(mc, args):
    '''Update the alarm state.'''
    fields = {}
    fields['alarm_id'] = args.id
    if args.state.upper() not in state_types:
            errmsg = ('Invalid state, not one of [' +
                      ', '.join(state_types) + ']')
            print(errmsg)
            return
    fields['state'] = args.state
    fields['lifecycle_state'] = args.lifecycle_state
    fields['link'] = args.link
    try:
        alarm = mc.alarms.update(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print(jsonutils.dumps(alarm, indent=2))


@utils.arg('id', metavar='<ALARM_ID>',
           help='The ID of the alarm.')
@utils.arg('--state', metavar='<ALARM_STATE>',
           help='ALARM_STATE is one of [UNDETERMINED, OK, ALARM].')
@utils.arg('--lifecycle-state', metavar='<LIFECYCLE_STATE>',
           help='The lifecycle state of the alarm.')
@utils.arg('--link', metavar='<LINK>',
           help='A link to an external resource with information about the alarm.')
def do_alarm_patch(mc, args):
    '''Patch the alarm state.'''
    fields = {}
    fields['alarm_id'] = args.id
    if args.state:
        if args.state.upper() not in state_types:
            errmsg = ('Invalid state, not one of [' +
                      ', '.join(state_types) + ']')
            print(errmsg)
            return
        fields['state'] = args.state
    if args.lifecycle_state:
        fields['lifecycle_state'] = args.lifecycle_state
    if args.link:
        fields['link'] = args.link
    try:
        alarm = mc.alarms.patch(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print(jsonutils.dumps(alarm, indent=2))


@utils.arg('id', metavar='<ALARM_ID>',
           help='The ID of the alarm.')
def do_alarm_delete(mc, args):
    '''Delete the alarm.'''
    fields = {}
    fields['alarm_id'] = args.id
    try:
        mc.alarms.delete(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        print('Successfully deleted alarm')


def output_alarm_history(args, alarm_history):
    if args.json:
            print(utils.json_formatter(alarm_history))
            return
    # format output
    cols = ['alarm_id', 'new_state', 'old_state', 'reason',
            'reason_data', 'metric_name', 'metric_dimensions', 'timestamp']
    formatters = {
        'alarm_id': lambda x: x['alarm_id'],
        'new_state': lambda x: x['new_state'],
        'old_state': lambda x: x['old_state'],
        'reason': lambda x: x['reason'],
        'reason_data': lambda x: x['reason_data'],
        'metric_name': lambda x: format_metric_name(x['metrics']),
        'metric_dimensions': lambda x: format_metric_dimensions(x['metrics']),
        'timestamp': lambda x: x['timestamp'],
    }
    if isinstance(alarm_history, list):
        # print the list
        utils.print_list(alarm_history, cols, formatters=formatters)
    else:
        # add the dictionary to a list, so print_list works
        alarm_list = list()
        alarm_list.append(alarm_history)
        utils.print_list(alarm_list, cols, formatters=formatters)


@utils.arg('--alarm-definition-id', metavar='<ALARM_DEFINITION_ID>',
           help='The ID of the alarm definition.')
@utils.arg('--metric-name', metavar='<METRIC_NAME>',
           help='Name of the metric.')
@utils.arg('--metric-dimensions', metavar='<KEY1=VALUE1,KEY2,KEY3=VALUE2...>',
           help='key value pair used to specify a metric dimension or '
                'just key to select all values of that dimension.'
                'This can be specified multiple times, or once with parameters '
                'separated by a comma. '
                'Dimensions need quoting when they contain special chars [&,(,),{,},>,<] '
                'that confuse the CLI parser.',
           action='append')
@utils.arg('--state', metavar='<ALARM_STATE>',
           help='ALARM_STATE is one of [UNDETERMINED, OK, ALARM].')
@utils.arg('--severity', metavar='<SEVERITY>',
           help='Severity is one of ["LOW", "MEDIUM", "HIGH", "CRITICAL"].')
@utils.arg('--state-updated-start-time', metavar='<UTC_STATE_UPDATED_START>',
           help='Return all alarms whose state was updated on or after the time specified.')
@utils.arg('--lifecycle-state', metavar='<LIFECYCLE_STATE>',
           help='The lifecycle state of the alarm.')
@utils.arg('--link', metavar='<LINK>',
           help='The link to external data associated with the alarm.')
@utils.arg('--group-by', metavar='<GROUP_BY>',
           help='Comma separated list of one or more fields to group the results by. '
                'Group by is one or more of [alarm_definition_id, name, state, link, '
                'lifecycle_state, metric_name, dimension_name, dimension_value].')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum limit.')
def do_alarm_count(mc, args):
    '''Count alarms.'''
    fields = {}
    if args.alarm_definition_id:
        fields['alarm_definition_id'] = args.alarm_definition_id
    if args.metric_name:
        fields['metric_name'] = args.metric_name
    if args.metric_dimensions:
        fields['metric_dimensions'] = utils.format_dimensions_query(args.metric_dimensions)
    if args.state:
        if args.state.upper() not in state_types:
            errmsg = ('Invalid state, not one of [' +
                      ', '.join(state_types) + ']')
            print(errmsg)
            return
        fields['state'] = args.state
    if args.severity:
        if not _validate_severity(args.severity):
            return
        fields['severity'] = args.severity
    if args.state_updated_start_time:
        fields['state_updated_start_time'] = args.state_updated_start_time
    if args.lifecycle_state:
        fields['lifecycle_state'] = args.lifecycle_state
    if args.link:
        fields['link'] = args.link
    if args.group_by:
        group_by = args.group_by.split(',')
        if not set(group_by).issubset(set(group_by_types)):
            errmsg = ('Invalid group-by, one or more values not in [' +
                      ','.join(group_by_types) + ']')
            print(errmsg)
            return
        fields['group_by'] = args.group_by
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    try:
        counts = mc.alarms.count(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        if args.json:
            print(utils.json_formatter(counts))
            return
        cols = counts['columns']

        utils.print_list(counts['counts'], [i for i in range(len(cols))],
                         field_labels=cols)


@utils.arg('id', metavar='<ALARM_ID>',
           help='The ID of the alarm.')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum limit.')
def do_alarm_history(mc, args):
    '''Alarm state transition history.'''
    fields = {}
    fields['alarm_id'] = args.id
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    try:
        alarm = mc.alarms.history(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        output_alarm_history(args, alarm)


@utils.arg('--dimensions', metavar='<KEY1=VALUE1,KEY2=VALUE2...>',
           help='key value pair used to specify a metric dimension. '
           'This can be specified multiple times, or once with parameters '
           'separated by a comma. '
           'Dimensions need quoting when they contain special chars [&,(,),{,},>,<] '
           'that confuse the CLI parser.',
           action='append')
@utils.arg('--starttime', metavar='<UTC_START_TIME>',
           help='measurements >= UTC time. format: 2014-01-01T00:00:00Z. OR'
                ' format: -120 (previous 120 minutes).')
@utils.arg('--endtime', metavar='<UTC_END_TIME>',
           help='measurements <= UTC time. format: 2014-01-01T00:00:00Z.')
@utils.arg('--offset', metavar='<OFFSET LOCATION>',
           help='The offset used to paginate the return data.')
@utils.arg('--limit', metavar='<RETURN LIMIT>',
           help='The amount of data to be returned up to the API maximum limit.')
def do_alarm_history_list(mc, args):
    '''List alarms state history.'''
    fields = {}
    if args.dimensions:
        fields['dimensions'] = utils.format_parameters(args.dimensions)
    if args.starttime:
        _translate_starttime(args)
        fields['start_time'] = args.starttime
    if args.endtime:
        fields['end_time'] = args.endtime
    if args.limit:
        fields['limit'] = args.limit
    if args.offset:
        fields['offset'] = args.offset
    try:
        alarm = mc.alarms.history_list(**fields)
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        output_alarm_history(args, alarm)


def do_notification_type_list(mc, args):
    '''List notification types supported by monasca.'''

    try:
        notification_types = mc.notificationtypes.list()
    except (osc_exc.ClientException, k_exc.HttpError) as he:
        raise osc_exc.CommandError('%s\n%s' % (he.message, he.details))
    else:
        if args.json:
            print(utils.json_formatter(notification_types))
            return
        else:
            formatters = {'types': lambda x: x["type"]}
            # utils.print_list(notification_types['types'], ["types"], formatters=formatters)
            utils.print_list(notification_types, ["types"], formatters=formatters)


def _translate_starttime(args):
    if args.starttime[0] == '-':
        deltaT = time.time() + (int(args.starttime) * 60)
        utc = str(datetime.datetime.utcfromtimestamp(deltaT))
        utc = utc.replace(" ", "T")[:-7] + 'Z'
        args.starttime = utc


def _arg_split_patch_update(arg, patch=False):
    if patch:
        arg = ','.join(arg)
    if not arg or arg == "[]":
        arg_split = []
    else:
        arg_split = arg.split(',')
    return arg_split
