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
import os
import sys
import textwrap
import uuid

import prettytable
import six
import yaml

from monascaclient import exc

from oslo_serialization import jsonutils
from oslo_utils import importutils

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


def link_formatter(links):
    return '\n'.join([l.get('href', '') for l in links or []])


def json_formatter(js):
    return (jsonutils.dumps(js, indent=2, ensure_ascii=False)).encode('utf-8')


def text_wrap_formatter(d):
    return '\n'.join(textwrap.wrap(d or '', 55))


def newline_list_formatter(r):
    return '\n'.join(r or [])


def print_list(objs, fields, field_labels=None, formatters={}, sortby=None):
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
    if sortby is None:
        print(pt.get_string().encode('utf-8'))
    else:
        print(pt.get_string(sortby=field_labels[sortby]).encode('utf-8'))


def print_dict(d, formatters={}):
    pt = prettytable.PrettyTable(['Property', 'Value'],
                                 caching=False, print_empty=False)
    pt.align = 'l'

    for field in d.keys():
        if field in formatters:
            pt.add_row([field, formatters[field](d[field])])
        else:
            pt.add_row([field, d[field]])
    print(pt.get_string(sortby='Property').encode('utf-8'))


def find_resource(manager, name_or_id):
    """Helper for the _find_* methods."""
    # first try to get entity as integer id
    try:
        if isinstance(name_or_id, int) or name_or_id.isdigit():
            return manager.get(int(name_or_id))
    except exc.NotFound:
        pass

    # now try to get entity as uuid
    try:
        uuid.UUID(str(name_or_id))
        return manager.get(name_or_id)
    except (ValueError, exc.NotFound):
        pass

    # finally try to find entity by name
    try:
        return manager.find(name=name_or_id)
    except exc.NotFound:
        msg = "No %s with a name or ID of '%s' exists." % \
              (manager.resource_class.__name__.lower(), name_or_id)
        raise exc.CommandError(msg)


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.
    """
    for v in vars:
        value = os.environ.get(v)
        if value:
            return value
    return kwargs.get('default', None)


def import_versioned_module(version, submodule=None):
    module = 'monascaclient.v%s' % version
    if submodule:
        module = '.'.join((module, submodule))
    return importutils.import_module(module)


def exit(msg=''):
    if msg:
        print(msg.encode('utf-8'), file=sys.stderr)
    sys.exit(1)


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
            (n, v) = p.split(('='), 1)
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


def format_output(output, format='yaml'):
    """Format the supplied dict as specified."""
    output_format = format.lower()
    try:
        return supported_formats[output_format](output)
    except KeyError:
        raise exc.HTTPUnsupported("The format(%s) is unsupported."
                                  % output_format)


def format_dimensions(dict):
    return ('dimensions: {\n' + format_dict(dict) + '\n}')


def format_expression_data(dict):
    # takes an dictionary containing a dict
    string_list = list()
    for k, v in dict.items():
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
        if isinstance(k, unicode):
            key = k.encode('utf-8')
        else:
            key = k
        string_list.append(key)
    return '\n'.join(string_list)


def set_env_variables(kwargs):
    environment_variables = {
        'username': 'OS_USERNAME',
        'password': 'OS_PASSWORD',
        'token': 'OS_AUTH_TOKEN',
        'auth_url': 'OS_AUTH_URL',
        'service_type': 'OS_SERVICE_TYPE',
        'endpoint_type': 'OS_ENDPOINT_TYPE',
        'os_cacert': 'OS_CACERT',
        'user_domain_id': 'OS_USER_DOMAIN_ID',
        'user_domain_name': 'OS_USER_DOMAIN_NAME',
        'project_id': 'OS_PROJECT_ID',
        'project_name': 'OS_PROJECT_NAME',
        'domain_id': 'OS_DOMAIN_ID',
        'domain_name': 'OS_DOMAIN_NAME',
        'region_name': 'OS_REGION_NAME'
    }
    for k, v in six.iteritems(environment_variables):
        if k not in kwargs:
            kwargs[k] = env(v)
