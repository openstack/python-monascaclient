# (C) Copyright 2014-2016 Hewlett Packard Enterprise Development Company LP
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

from __future__ import print_function

import numbers

import prettytable
import six
import yaml

from osc_lib import exceptions as exc

from oslo_serialization import jsonutils

supported_formats = {
    "json": lambda x: jsonutils.dumps(x, indent=2),
    "yaml": yaml.safe_dump
}


# Decorator for cli-args
def arg(*args, **kwargs):
    def _decorator(func):
        # Because of the semantics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        func.__dict__.setdefault('arguments', []).insert(0, (args, kwargs))
        return func
    return _decorator


def json_formatter(js):
    formatter = (jsonutils.dumps(js, indent=2, ensure_ascii=False))
    return formatter if six.PY3 else formatter.encode('utf-8')


def print_list(objs, fields, field_labels=None, formatters=None, sortby=None):
    if formatters is None:
        formatters = {}

    field_labels = field_labels or fields
    pt = prettytable.PrettyTable([f for f in field_labels],
                                 caching=False, print_empty=False)
    pt.align = 'l'

    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            elif isinstance(field, int):
                row.append(o[field])
            else:
                data = getattr(o, field, None) or ''
                row.append(data)
        pt.add_row(row)
    field_to_sort_by = field_labels[sortby] if sortby else None
    pt_string = pt.get_string(sortby=field_to_sort_by)
    print(pt_string if six.PY3 else pt_string.encode('utf-8'))


def print_dict(d, formatters=None):
    if formatters is None:
        formatters = {}
    pt = prettytable.PrettyTable(['Property', 'Value'],
                                 caching=False, print_empty=False)
    pt.align = 'l'

    for field in d:
        if field in formatters:
            pt.add_row([field, formatters[field](d[field])])
        else:
            pt.add_row([field, d[field]])

    pt_string = pt.get_string(sortby='Property')
    print(pt_string if six.PY3 else pt_string.encode('utf-8'))


def format_parameters(params):
    '''Reformat parameters into dict of format expected by the API.'''

    if not params:
        return {}

    # expect multiple invocations of --parameters but fall back
    # to ; delimited if only one --parameters is specified
    if len(params) == 1:
        if params[0].find(';') != -1:  # found
            params = params[0].split(';')
        else:
            params = params[0].split(',')

    parameters = {}
    for p in params:
        try:
            (n, v) = p.split('=', 1)
        except ValueError:
            msg = '%s(%s). %s.' % ('Malformed parameter', p,
                                   'Use the key=value format')
            raise exc.CommandError(msg)

        if n not in parameters:
            parameters[n] = v
        else:
            if not isinstance(parameters[n], list):
                parameters[n] = [parameters[n]]
            parameters[n].append(v)

    return parameters


def format_dimensions_query(dims):
    if not dims:
        return {}

    # expect multiple invocations of --parameters but fall back
    # to ; delimited if only one --parameters is specified
    if len(dims) == 1:
        if dims[0].find(';') != -1:  # found
            dims = dims[0].split(';')
        else:
            dims = dims[0].split(',')

    dimensions = {}
    for p in dims:
        try:
            (n, v) = p.split('=', 1)
        except ValueError:
            n = p
            v = ""

        dimensions[n] = v

    return dimensions


def format_dimensions(dict):
    return 'dimensions: {\n' + format_dict(dict) + '\n}'


def format_expression_data(data):
    # takes an dictionary containing a dict
    string_list = list()
    for k, v in data.items():
        if k == 'dimensions':
            dim_str = format_dimensions(v)
            string_list.append(dim_str)
        else:
            if isinstance(v, numbers.Number):
                d_str = k + ': ' + str(v)
            else:
                d_str = k + ': ' + v
            string_list.append(d_str)
    return '\n'.join(string_list)


def format_dictlist(dict_list):
    # takes list of dictionaries to format for output
    string_list = list()
    for mdict in dict_list:
        kv_list = list()
        for k, v in sorted(mdict.items()):
            kv_str = k + ':' + str(v)
            kv_list.append(kv_str)
        # a string of comma separated k:v
        this_dict_str = ','.join(kv_list)
        string_list.append(this_dict_str)
    return '\n'.join(string_list)


def format_dict(dict):
    # takes a dictionary to format for output
    dstring_list = list()
    for k, v in dict.items():
        if isinstance(v, numbers.Number):
            d_str = k + ': ' + str(v)
        else:
            d_str = k + ': ' + v
        dstring_list.append(d_str)
    return '\n'.join(dstring_list)


def format_list(in_list):
    string_list = list()
    for k in in_list:
        if isinstance(k, six.text_type):
            key = k.encode('utf-8')
        else:
            key = k
        string_list.append(key)
    return b'\n'.join(string_list)
