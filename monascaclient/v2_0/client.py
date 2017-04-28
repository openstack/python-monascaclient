# (C) Copyright 2014-2015 Hewlett Packard Enterprise Development Company LP
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

from osc_lib.api import api

from monascaclient.v2_0 import alarm_definitions as ad
from monascaclient.v2_0 import alarms
from monascaclient.v2_0 import metrics
from monascaclient.v2_0 import notifications
from monascaclient.v2_0 import notificationtypes as nt


class Client(object):
    def __init__(self, *args, **kwargs):
        """Initialize a new http client for the monasca API."""

        client = MonascaApi(*args, **kwargs)

        self.metrics = metrics.MetricsManager(client)
        self.notifications = notifications.NotificationsManager(client)
        self.alarms = alarms.AlarmsManager(client)
        self.alarm_definitions = ad.AlarmDefinitionsManager(client)
        self.notificationtypes = nt.NotificationTypesManager(client)


class MonascaApi(api.BaseAPI):
    SERVICE_TYPE = "monitoring"
