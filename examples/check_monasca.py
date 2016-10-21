#!/usr/bin/env python

#
# (C) Copyright 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

import getopt
import os
import sys

from monascaclient import client


def usage():
    usage = """
    Requires services.osrc variables in bash environment (OS_USERNAME etc).

    check_monasca -d <dimension> -v <value>
        -h --help                 Prints this
        -d dimension              Dimension to filter on
        -v value                  Value of dimension

    Examples

    check_monasca -d hostname -v test-c0-m1-mgmt # Retrieve all alarms for a host
    check_monasca -d service -v nova # Retrieve all nova alarms
    """
    print(usage)


def get_keystone_creds():
    creds = {'username': os.environ['OS_USERNAME'], 'password': os.environ['OS_PASSWORD'],
             'auth_url': os.environ['OS_AUTH_URL'], 'project_name': os.environ['OS_PROJECT_NAME'],
             'endpoint': os.environ['OS_MONASCA_URL'], 'os_cacert': os.environ['OS_CACERT']}
    return creds


def format_alarm(alarm):
    output = "%s %s ( Metric = %s)" % (
        alarm['metrics'][0]['dimensions']['hostname'],
        alarm['alarm_definition']['name'],
        alarm['metrics'][0]['name'])
    if "process." in alarm['metrics'][0]['name']:
        output += "-%s," % (alarm['metrics'][0]['dimensions']['process_name'])
    if "disk." in alarm['metrics'][0]['name']:
        output += "-%s," % (alarm['metrics'][0]['dimensions']['mount_point'])
    output += ","
    return output


def main(argv):
    # Initialise Variables
    warns = 0
    crits = 0
    warns_output = ""
    crits_output = ""
    dimension = ""
    dim_value = ""

    # Test parameters
    try:
        opts, args = getopt.getopt(argv, "h::d:v:", ["dimension=", "value="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-d", "--dimension"):
            dimension = arg
        elif opt in ("-v", "--value"):
            dim_value = arg

    if dimension == "" or dim_value == "":
        usage()
        sys.exit(2)

    # Set the api version of monasca-api
    api_version = '2_0'
    creds = get_keystone_creds()

    # Build request
    dimensions = {}
    dimensions[dimension] = dim_value

    fields = {}
    fields['metric_dimensions'] = dimensions
    monasca_client = client.Client(api_version, **creds)
    body = monasca_client.alarms.list(**fields)

    # Process retrieved alarms
    # Note Monasca has state and severity, these are mapped to Nagios values as
    # State ALARM and severity = LOW or MEDIUM is Nagios Warning
    # State = UNDERTERMINED is Nagios Warning
    # State ALARM and severity = HIGH it Nagios Critical

    for alarm in body:
        if alarm['lifecycle_state'] != "RESOLVED":
            if (alarm['state'] == "ALARM" and
                (alarm['alarm_definition']['severity'] == "LOW" or
                    alarm['alarm_definition']['severity'] == "MEDIUM")):
                warns += 1
                warns_output += format_alarm(alarm)
            if alarm['state'] == "UNDETERMINED":
                warns += 1
                warns_output += format_alarm(alarm)
            if alarm['state'] == "ALARM" and alarm['alarm_definition']['severity'] == "HIGH":
                crits += 1
                crits_output += format_alarm(alarm)

    if warns == 0 and crits == 0:
        print("OK")
        return
    elif warns > 0 and crits == 0:
        print(str(warns) + " WARNING - " + warns_output)
        sys.exit(1)
    elif crits > 0:
        print(str(crits) + " CRITICAL - " + crits_output + str(warns) + " WARNING - " + warns_output)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
