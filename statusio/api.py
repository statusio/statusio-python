#!/usr/bin/env python

"""A library that provides a Python interface to the Status.io API"""
from __future__ import division
from __future__ import print_function

import sys
import gzip
import time
import types
import base64
import re
import datetime
from calendar import timegm
import requests
import io

from past.utils import old_div

try:
    # python 3
    from urllib.parse import urlparse, urlunparse, urlencode
    from urllib.request import urlopen
    from urllib.request import __version__ as urllib_version
except ImportError:
    from urlparse import urlparse, urlunparse
    from urllib2 import urlopen
    from urllib import urlencode
    from urllib import __version__ as urllib_version

from statusio import (__version__, json)


class Api(object):
    """A python interface into the Status.io API

    Example usage:

      Simples example

        >>> import statusio
        >>> api = statusio.Api(API_ID, API_KEY)
        >>> result = api.StatusSummary(STATUSPAGE_ID)
        >>> print(result)

      There are many other methods, including:

        >>> api.ComponentList(statuspage_id)
        >>> api.ComponentStatusUpdate(statuspage_id, component, container, details, current_status)
        >>> api.IncidentList(statuspage_id)
        >>> api.IncidentListByID(statuspage_id)
        >>> api.IncidentMessage(statuspage_id, message_id)
        >>> api.IncidentSingle(statuspage_id, incident_id)
        >>> api.IncidentCreate(statuspage_id, infrastructure_affected, incident_name, incident_details, current_status, current_state, notify_email="0", notify_sms="0", notify_webhook="0", social="0", irc="0", hipchat="0", msteams="0", slack="0", all_infrastructure_affected="0", message_subject="Status Notification")
        >>> api.IncidentUpdate(statuspage_id, incident_id, incident_details, current_status, current_state, notify_email="0", notify_sms="0", notify_webhook="0", social="0", irc="0", hipchat="0", msteams="0", slack="0", message_subject="Status Notification")
        >>> api.IncidentResolve(statuspage_id, incident_id, incident_details, current_status, current_state, notify_email="0", notify_sms="0", notify_webhook="0", social="0", irc="0", hipchat="0", msteams="0", slack="0", message_subject="Status Notification")
        >>> api.IncidentDelete(statuspage_id, incident_id)
        >>> api.MaintenanceList(statuspage_id)
        >>> api.MaintenanceListByID(statuspage_id)
        >>> api.MaintenanceMessage(statuspage_id, message_id)
        >>> api.MaintenanceSingle(statuspage_id, maintenance_id)
        >>> api.MaintenanceSchedule(statuspage_id, infrastructure_affected, maintenance_name, maintenance_details, date_planned_start, time_planned_start, date_planned_end, time_planned_end, automation="0", all_infrastructure_affected="0", maintenance_notify_now="0", maintenance_notify_1_hr="0", maintenance_notify_24_hr="0", maintenance_notify_72_hr="0", message_subject="Status Notification")
        >>> api.MaintenanceStart(statuspage_id, maintenance_id, maintenance_details, notify_email="0", notify_sms="0", notify_webhook="0", social="0", irc="0", hipchat="0", msteams="0", slack="0", message_subject="Status Notification")
        >>> api.MaintenanceUpdate(statuspage_id, maintenance_id, maintenance_details, notify_email="0", notify_sms="0", notify_webhook="0", social="0", irc="0", hipchat="0", msteams="0", slack="0", message_subject="Status Notification")
        >>> api.MaintenanceFinish(statuspage_id, maintenance_id, maintenance_details, notify_email="0", notify_sms="0", notify_webhook="0", social="0", irc="0", hipchat="0", msteams="0", slack="0", message_subject="Status Notification")
        >>> api.MaintenanceDelete(statuspage_id, maintenance_id)
        >>> api.MetricUpdate(statuspage_id, metric_id, day_avg, day_start, day_dates, day_values, week_avg, week_start, week_dates, week_values, month_avg, month_start, month_dates, month_values)
        >>> api.StatusSummary(statuspage_id)
        >>> api.SubscriberList(statuspage_id)
        >>> api.SubscriberAdd(statuspage_id, method, address, silent='1', granular='')
        >>> api.SubscriberUpdate(statuspage_id, subscriber_id, address, granular='')
        >>> api.SubscriberRemove(statuspage_id, subscriber_id)
    """

    def __init__(self,
                 api_id,
                 api_key,
                 version=2,
                 base_url='https://api.status.io'
                 ):
        """Instantiate a new statusio.Api object.

        Args:
          api_id:
            Your Status.io API ID.
          api_key:
            Your Status.io API KEY.
          version:
            API version number. [Optional]
          base_url:
            API base URL. [Optional]
        """
        self._api_id = api_id
        self._api_key = api_key
        self.base_url = '%s/v%d' % (base_url, version)

    def ComponentList(self, statuspage_id):
        """List all components.

           Args:
             statuspage_id:
               Status page ID

           Returns:
             A JSON object.
        """
        url = '%s/component/list/%s' % (self.base_url, statuspage_id)
        resp = self._RequestUrl(url, 'GET')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def ComponentStatusUpdate(self,
                              statuspage_id,
                              component,
                              container,
                              details,
                              current_status):
        """Update the status of a component on the fly without creating an incident or maintenance.

           Args:
             statuspage_id:
               Status page ID
             component:
               ID of affected component
             container:
               ID of affected container
             details:
               A brief message describing this update
             current_status:
               Any numeric status code.

           Returns:
             A JSON object.
        """
        url = '%s/component/status/update' % self.base_url
        resp = self._RequestUrl(url, 'POST', data={
            'statuspage_id': statuspage_id,
            'component': component,
            'container': container,
            'details': details,
            'current_status': current_status
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def IncidentList(self, statuspage_id):
        """List all active and resolved incidents.

           Args:
             statuspage_id:
               Status page ID

           Returns:
             A JSON object.
        """
        url = '%s/incident/list/%s' % (self.base_url, statuspage_id)
        resp = self._RequestUrl(url, 'GET')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def IncidentListByID(self, statuspage_id):
        """List all active and resolved incidents by ID.

           Args:
             statuspage_id:
               Status page ID

           Returns:
             A JSON object.
        """
        url = '%s/incidents/%s' % (self.base_url, statuspage_id)
        resp = self._RequestUrl(url, 'GET')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def IncidentMessage(self,
                        statuspage_id,
                        message_id):
        """Display incident message.

           Args:
             statuspage_id:
               Status page ID
             message_id:
               Message ID

           Returns:
             A JSON object.
        """
        url = '%s/incident/message/%s/%s' % (self.base_url,
                                             statuspage_id, message_id)
        resp = self._RequestUrl(url, 'GET')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def IncidentSingle(self,
                        statuspage_id,
                        incident_id):
        """Get single incident.

           Args:
             statuspage_id:
               Status page ID
             incident_id:
               Incident ID

           Returns:
             A JSON object.
        """
        url = '%s/incident/%s/%s' % (self.base_url,
                                             statuspage_id, incident_id)
        resp = self._RequestUrl(url, 'GET')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def IncidentCreate(self,
                       statuspage_id,
                       infrastructure_affected,
                       incident_name,
                       incident_details,
                       current_status,
                       current_state,
                       notify_email="0",
                       notify_sms="0",
                       notify_webhook="0",
                       social="0",
                       irc="0",
                       hipchat="0",
                       msteams="0",
                       slack="0",
                       all_infrastructure_affected="0",
                       message_subject="Status Notification"):
        """Create a new incident.

           Args:
             statuspage_id:
               Status page ID
             infrastructure_affected:
               ID of each affected component and container combo
             all_infrastructure_affected:
               Include all components and containers
             incident_name:
               A descriptive title for the incident
             incident_details:
               Message describing this incident
             current_status:
               The status of the components and containers affected by this incident
             current_state:
               The state of this incident
             notify_email:
               Notify email subscribers (1 = Send notification)
             notify_sms:
               Notify SMS subscribers (1 = Send notification)
             notify_webhook:
               Notify webhook subscribers (1 = Send notification)
             social:
               Automatically Tweet this update. (1 = Send Tweet)
             irc:
               Notify IRC channel (1 = Send notification)
             hipchat:
               Notify HipChat room (1 = Send notification)
             msteams:
               Notify Microsoft Teams channels (1 = Send notification)
             slack:
               Notify Slack channels (1 = Send notification)
             message_subject:
               The message subject for email notifications

           Returns:
             A JSON object.
        """
        url = '%s/incident/create' % self.base_url
        resp = self._RequestUrl(url, 'POST', {
            'statuspage_id': statuspage_id,
            'infrastructure_affected': infrastructure_affected,
            'incident_name': incident_name,
            'incident_details': incident_details,
            'current_status': current_status,
            'current_state': current_state,
            'notify_email': notify_email,
            'notify_sms': notify_sms,
            'notify_webhook': notify_webhook,
            'social': social,
            'irc': irc,
            'hipchat': hipchat,
            'msteams': msteams,
            'slack': slack,
            'all_infrastructure_affected': all_infrastructure_affected,
            'message_subject': message_subject
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def IncidentUpdate(self,
                       statuspage_id,
                       incident_id,
                       incident_details,
                       current_status,
                       current_state,
                       notify_email="0",
                       notify_sms="0",
                       notify_webhook="0",
                       social="0",
                       irc="0",
                       hipchat="0", 
                       msteams="0",
                       slack="0",
                       message_subject="Status Notification"):
        """Update an existing incident

           Args:
             statuspage_id:
               Status page ID
             incident_id:
               Incident ID
             incident_details:
               Message describing this incident
             current_status:
               The status of the components and containers affected by this incident
             current_state:
               The state of this incident
             notify_email:
               Notify email subscribers (1 = Send notification)
             notify_sms:
               Notify SMS subscribers (1 = Send notification)
             notify_webhook:
               Notify webhook subscribers (1 = Send notification)
             social:
               Automatically Tweet this update. (1 = Send Tweet)
             irc:
               Notify IRC channel (1 = Send notification)
             hipchat:
               Notify HipChat room (1 = Send notification)
             msteams:
               Notify Microsoft Teams channels (1 = Send notification)
             slack:
               Notify Slack channels (1 = Send notification)
             message_subject:
               The message subject for email notifications

           Returns:
             A JSON object.
        """
        url = '%s/incident/update' % self.base_url
        resp = self._RequestUrl(url, 'POST', {
            'statuspage_id': statuspage_id,
            'incident_id': incident_id,
            'incident_details': incident_details,
            'current_status': current_status,
            'current_state': current_state,
            'notify_email': notify_email,
            'notify_sms': notify_sms,
            'notify_webhook': notify_webhook,
            'social': social,
            'irc': irc,
            'hipchat': hipchat,
            'msteams': msteams,
            'slack': slack,
            'message_subject': message_subject
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def IncidentResolve(self,
                        statuspage_id,
                        incident_id,
                        incident_details,
                        current_status,
                        current_state,
                        notify_email="0",
                        notify_sms="0",
                        notify_webhook="0",
                        social="0",
                        irc="0",
                        hipchat="0",
                        msteams="0",
                        slack="0",
                        message_subject="Status Notification"):
        """Resolve an existing incident. The incident will be shown in the history instead of on the main page.

           Args:
             statuspage_id:
               Status page ID
             incident_id:
               Incident ID
             incident_details:
               Message describing this incident
             current_status:
               The status of the components and containers affected by this incident
             current_state:
               The state of this incident
             notify_email:
               Notify email subscribers (1 = Send notification)
             notify_sms:
               Notify SMS subscribers (1 = Send notification)
             notify_webhook:
               Notify webhook subscribers (1 = Send notification)
             social:
               Automatically Tweet this update. (1 = Send Tweet)
             irc:
               Notify IRC channel (1 = Send notification)
             hipchat:
               Notify HipChat room (1 = Send notification)
             msteams:
               Notify Microsoft Teams channels (1 = Send notification)
             slack:
               Notify Slack channels (1 = Send notification)
             message_subject
               The message subject for email notifications

           Returns:
             A JSON object.
        """
        url = '%s/incident/resolve' % self.base_url
        resp = self._RequestUrl(url, 'POST', {
            'statuspage_id': statuspage_id,
            'incident_id': incident_id,
            'incident_details': incident_details,
            'current_status': current_status,
            'current_state': current_state,
            'notify_email': notify_email,
            'notify_sms': notify_sms,
            'notify_webhook': notify_webhook,
            'social': social,
            'irc': irc,
            'hipchat': hipchat,
            'msteams': msteams,
            'slack': slack,
            'message_subject': message_subject
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def IncidentDelete(self,
                       statuspage_id,
                       incident_id):
        """Delete an existing incident. The incident will be deleted forever and cannot be recovered.

           Args:
             statuspage_id:
               Status page ID
             incident_id:
               Incident ID

           Returns:
             A JSON object.
        """
        url = '%s/incident/delete' % self.base_url
        resp = self._RequestUrl(url, 'POST', {
            'statuspage_id': statuspage_id,
            'incident_id': incident_id
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def MaintenanceList(self, statuspage_id):
        """List all active, resolved and upcoming maintenances

           Args:
             statuspage_id:
               Status page ID

           Returns:
             A JSON object.
        """
        url = '%s/maintenance/list/%s' % (self.base_url, statuspage_id)
        resp = self._RequestUrl(url, 'GET')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def MaintenanceListByID(self, statuspage_id):
        """List all active, resolved and upcoming maintenances by ID

           Args:
             statuspage_id:
               Status page ID

           Returns:
             A JSON object.
        """
        url = '%s/maintenances/%s' % (self.base_url, statuspage_id)
        resp = self._RequestUrl(url, 'GET')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def MaintenanceMessage(self,
                           statuspage_id,
                           message_id):
        """Display maintenance message

           Args:
             statuspage_id:
               Status page ID
             incident_id:
               Message ID

           Returns:
             A JSON object.
        """
        url = '%s/maintenance/message/%s/%s' % (
            self.base_url, statuspage_id, message_id)
        resp = self._RequestUrl(url, 'GET')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def MaintenanceSingle(self,
                           statuspage_id,
                           maintenance_id):
        """Display maintenance message

           Args:
             statuspage_id:
               Status page ID
             maintenance_id:
               Maintenance ID

           Returns:
             A JSON object.
        """
        url = '%s/maintenance/%s/%s' % (
            self.base_url, statuspage_id, maintenance_id)
        resp = self._RequestUrl(url, 'GET')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def MaintenanceSchedule(self,
                            statuspage_id,
                            infrastructure_affected,
                            maintenance_name,
                            maintenance_details,
                            date_planned_start,
                            time_planned_start,
                            date_planned_end,
                            time_planned_end,
                            automation="0",
                            all_infrastructure_affected="0",
                            maintenance_notify_now="0",
                            maintenance_notify_1_hr="0",
                            maintenance_notify_24_hr="0",
                            maintenance_notify_72_hr="0",
                            message_subject="Status Notification"):
        """Schedule a new maintenance

           Args:
             statuspage_id:
               Status page ID
             infrastructure_affected:
               ID of each affected component and container combo
             maintenance_name:
               A descriptive title for this maintenance
             maintenance_details:
               Message describing this maintenance
             date_planned_start:
               Date maintenance is expected to start
             time_planned_start:
               Time maintenance is expected to start
             date_planned_end:
               Date maintenance is expected to end
             time_planned_end:
               Time maintenance is expected to end
             automation:
               Automatically start and end the maintenance (default = 0)
             all_infrastructure_affected:
               Affect all components and containers (default = 0)
             maintenance_notify_now:
               Notify subscribers now (1 = Send notification)
             maintenance_notify_1_hr:
               Notify subscribers 1 hour before scheduled maintenance start time (1 = Send notification)
             maintenance_notify_24_hr:
               Notify subscribers 24 hours before scheduled maintenance start time (1 = Send notification)
             maintenance_notify_72_hr:
               Notify subscribers 72 hours before scheduled maintenance start time (1 = Send notification)
             message_subject:
               The message subject for email notifications

           Returns:
             A JSON object.
        """
        url = '%s/maintenance/schedule' % self.base_url
        resp = self._RequestUrl(url, 'POST', {
            'statuspage_id': statuspage_id,
            'infrastructure_affected': infrastructure_affected,
            'maintenance_name': maintenance_name,
            'maintenance_details': maintenance_details,
            'date_planned_start': date_planned_start,
            'time_planned_start': time_planned_start,
            'date_planned_end': date_planned_end,
            'time_planned_end': time_planned_end,
            'automation': automation,
            'all_infrastructure_affected': all_infrastructure_affected,
            'maintenance_notify_now': maintenance_notify_now,
            'maintenance_notify_1_hr': maintenance_notify_1_hr,
            'maintenance_notify_24_hr': maintenance_notify_24_hr,
            'maintenance_notify_72_hr': maintenance_notify_72_hr,
            'message_subject': message_subject
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def MaintenanceStart(self,
                         statuspage_id,
                         maintenance_id,
                         maintenance_details,
                         notify_email="0",
                         notify_sms="0",
                         notify_webhook="0",
                         social="0",
                         irc="0",
                         hipchat="0",
                         msteams="0",
                         slack="0",
                         message_subject="Maintenance Notification"):
        """Begin a scheduled maintenance now

           Args:
             statuspage_id:
               Status page ID
             maintenance_id:
               Maintenance ID
             maintenance_details:
               Message describing this maintenance update
             notify_email:
               Notify email subscribers (1 = Send notification)
             notify_sms:
               Notify SMS subscribers (1 = Send notification)
             notify_webhook:
               Notify webhook subscribers (1 = Send notification)
             social:
               Automatically Tweet this update. (1 = Send Tweet)
             irc:
               Notify IRC channel (1 = Send notification)
             hipchat:
               Notify HipChat room (1 = Send notification)
             msteams:
               Notify Microsoft Teams channels (1 = Send notification)
             slack:
               Notify Slack channels (1 = Send notification)
             message_subject:
               The message subject for email notifications

           Returns:
             A JSON object.
        """
        url = '%s/maintenance/start' % self.base_url
        resp = self._RequestUrl(url, 'POST', {
            'statuspage_id': statuspage_id,
            'maintenance_id': maintenance_id,
            'maintenance_details': maintenance_details,
            'notify_email': notify_email,
            'notify_sms': notify_sms,
            'notify_webhook': notify_webhook,
            'social': social,
            'irc': irc,
            'hipchat': hipchat,
            'msteams': msteams,
            'slack': slack,
            'message_subject': message_subject
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def MaintenanceUpdate(self,
                          statuspage_id,
                          maintenance_id,
                          maintenance_details,
                          notify_email="0",
                          notify_sms="0",
                          notify_webhook="0",
                          social="0",
                          irc="0",
                          hipchat="0",
                          msteams="0",
                          slack="0",
                          message_subject="Maintenance Notification"):
        """Update an active maintenance

           Args:
             statuspage_id:
               Status page ID
             maintenance_id:
               Maintenance ID
             maintenance_details:
               Message describing this maintenance update
             notify_email:
               Notify email subscribers (1 = Send notification)
             notify_sms:
               Notify SMS subscribers (1 = Send notification)
             notify_webhook:
               Notify webhook subscribers (1 = Send notification)
             social:
               Automatically Tweet this update. (1 = Send Tweet)
             irc:
               Notify IRC channel (1 = Send notification)
             hipchat:
               Notify HipChat room (1 = Send notification)
             msteams:
               Notify Microsoft Teams channels (1 = Send notification)
             slack:
               Notify Slack channels (1 = Send notification)
             message_subject:
               The message subject for email notifications

           Returns:
             A JSON object.
        """
        url = '%s/maintenance/update' % self.base_url
        resp = self._RequestUrl(url, 'POST', {
            'statuspage_id': statuspage_id,
            'maintenance_id': maintenance_id,
            'maintenance_details': maintenance_details,
            'notify_email': notify_email,
            'notify_sms': notify_sms,
            'notify_webhook': notify_webhook,
            'social': social,
            'irc': irc,
            'hipchat': hipchat,
            'msteams': msteams,
            'slack': slack,
            'message_subject': message_subject
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def MaintenanceFinish(self,
                          statuspage_id,
                          maintenance_id,
                          maintenance_details,
                          notify_email="0",
                          notify_sms="0",
                          notify_webhook="0",
                          social="0",
                          irc="0",
                          hipchat="0",
                          msteams="0",
                          slack="0",
                          message_subject="Maintenance Notification"):
        """Close an active maintenance. The maintenance will be moved to the history.

           Args:
             statuspage_id:
               Status page ID
             maintenance_id:
               Maintenance ID
             maintenance_details:
               Message describing this maintenance update
             notify_email:
               Notify email subscribers (1 = Send notification)
             notify_sms:
               Notify SMS subscribers (1 = Send notification)
             notify_webhook:
               Notify webhook subscribers (1 = Send notification)
             social:
               Automatically Tweet this update. (1 = Send Tweet)
             irc:
               Notify IRC channel (1 = Send notification)
             hipchat:
               Notify HipChat room (1 = Send notification)
             msteams:
               Notify Microsoft Teams channels (1 = Send notification)
             slack:
               Notify Slack channels (1 = Send notification)
             message_subject:
               The message subject for email notifications

           Returns:
             A JSON object.
        """
        url = '%s/maintenance/finish' % self.base_url
        resp = self._RequestUrl(url, 'POST', {
            'statuspage_id': statuspage_id,
            'maintenance_id': maintenance_id,
            'maintenance_details': maintenance_details,
            'notify_email': notify_email,
            'notify_sms': notify_sms,
            'notify_webhook': notify_webhook,
            'social': social,
            'irc': irc,
            'hipchat': hipchat,
            'msteams': msteams,
            'slack': slack,
            'message_subject': message_subject
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def MaintenanceDelete(self,
                          statuspage_id,
                          maintenance_id):
        """Delete an existing maintenance. The maintenance will be deleted forever and cannot be recovered.

           Args:
             statuspage_id:
               Status page ID
             maintenance_id:
               Maintenance ID

           Returns:
             A JSON object.
        """
        url = '%s/maintenance/delete' % self.base_url
        resp = self._RequestUrl(url, 'POST', {
            'statuspage_id': statuspage_id,
            'maintenance_id': maintenance_id
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def MetricUpdate(self,
                     statuspage_id,
                     metric_id,
                     day_avg,
                     day_start,
                     day_dates,
                     day_values,
                     week_avg,
                     week_start,
                     week_dates,
                     week_values,
                     month_avg,
                     month_start,
                     month_dates,
                     month_values):
        """Update custom metric data

           Args:
             statuspage_id:
               Status page ID
             metric_id:
               Metric ID
             day_avg:
               Average value for past 24 hours
             day_start:
               UNIX timestamp for start of metric timeframe
             day_dates:
               An array of timestamps for the past 24 hours (2014-03-28T05:43:00+00:00)
             day_values:
               An array of values matching the timestamps (Must be 24 values)
             week_avg:
               Average value for past 7 days
             week_start:
               UNIX timestamp for start of metric timeframe
             week_dates:
               An array of timestamps for the past 7 days (2014-03-28T05:43:00+00:00)
             week_values:
               An array of values matching the timestamps (Must be 7 values)
             month_avg:
               Average value for past 30 days
             month_start:
               UNIX timestamp for start of metric timeframe
             month_dates:
               An array of timestamps for the past 30 days (2014-03-28T05:43:00+00:00)
             month_values:
               An array of values matching the timestamps (Must be 30 values)

           Returns:
             A JSON object.
        """
        url = '%s/metric/update' % self.base_url
        resp = self._RequestUrl(url, 'POST', {
            'statuspage_id': statuspage_id,
            'metric_id': metric_id,
            'day_avg': day_avg,
            'day_start': day_start,
            'day_dates': day_dates,
            'day_values': day_values,
            'week_avg': week_avg,
            'week_start': week_start,
            'week_dates': week_dates,
            'week_values': week_values,
            'month_avg': month_avg,
            'month_start': month_start,
            'month_dates': month_dates,
            'month_values': month_values
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def StatusSummary(self, statuspage_id):
        """Show the summary status for all components and containers

           Args:
             statuspage_id:
               Status page ID

           Returns:
             A JSON object.
        """
        url = '%s/status/summary/%s' % (self.base_url, statuspage_id)
        resp = self._RequestUrl(url, 'GET')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def SubscriberList(self, statuspage_id):
        """List all subscribers

           Args:
             statuspage_id:
               Status page ID

           Returns:
             A JSON object.
        """
        url = '%s/subscriber/list/%s' % (self.base_url, statuspage_id)
        resp = self._RequestUrl(url, 'GET')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def SubscriberAdd(self,
                      statuspage_id,
                      method,
                      address,
                      silent='1',
                      granular=''):
        """Add a new subscriber

           Args:
             statuspage_id:
               Status page ID
             method:
               Communication method of subscriber. Valid methods are `email`, `sms` or `webhook`
             address:
               Subscriber address (SMS number must include country code ie. +1)
             silent:
               Suppress the welcome message ('1' = Do not send notification)
             granular:
               List of component_container combos

           Returns:
             A JSON object.
        """
        url = '%s/subscriber/add' % self.base_url
        resp = self._RequestUrl(url, 'POST', {
            'statuspage_id': statuspage_id,
            'method': method,
            'address': address,
            'silent': silent,
            'granular': granular,
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def SubscriberUpdate(self,
                         statuspage_id,
                         subscriber_id,
                         address,
                         granular=''):
        """Update existing subscriber

           Args:
             statuspage_id:
               Status page ID
             subscriber_id:
               SubscriberAdd ID
             address:
               Subscriber address (SMS number must include country code ie. +1)
             granular:
               List of component_container combos

           Returns:
             A JSON object.
        """
        url = '%s/subscriber/update' % self.base_url
        resp = self._RequestUrl(url, 'PATCH', {
            'statuspage_id': statuspage_id,
            'subscriber_id': subscriber_id,
            'address': address,
            'granular': granular,
        })
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def SubscriberRemove(self,
                         statuspage_id,
                         subscriber_id):
        """Delete subscriber

           Args:
             statuspage_id:
               Status page ID
             subscriber_id:
               Subscriber ID

           Returns:
             A JSON object.
        """
        url = '%s/subscriber/remove/%s/%s' % (
            self.base_url, statuspage_id, subscriber_id)
        resp = self._RequestUrl(url, 'DELETE')
        data = json.loads(resp.content.decode('utf-8'))
        return data

    def _BuildUrl(self, url, path_elements=None, extra_params=None):
        # Break url into constituent parts
        (scheme, netloc, path, params, query, fragment) = urlparse(url)

        # Add any additional path elements to the path
        if path_elements:
            # Filter out the path elements that have a value of None
            p = [i for i in path_elements if i]
            if not path.endswith('/'):
                path += '/'
            path += '/'.join(p)

        # Add any additional query parameters to the query string
        if extra_params and len(extra_params) > 0:
            extra_query = self._EncodeParameters(extra_params)
            # Add it to the existing query
            if query:
                query += '&' + extra_query
            else:
                query = extra_query

        # Return the rebuilt URL
        return urlunparse((scheme, netloc, path, params, query, fragment))

    def _Encode(self, s):
        if self._input_encoding:
            return str(s, self._input_encoding).encode('utf-8')
        else:
            return str(s).encode('utf-8')

    def _EncodeParameters(self, parameters):
        """Return a string in key=value&key=value form.

        Values of None are not included in the output string.

        Args:
          parameters:
            A dict of (key, value) tuples, where value is encoded as
            specified by self._encoding

        Returns:
          A URL-encoded string in "key=value&key=value" form
        """
        if parameters is None:
            return None
        else:
            return urlencode(dict([(k, self._Encode(v)) for k, v in list(
                parameters.items()) if v is not None]))

    def _EncodePostData(self, post_data):
        """Return a string in key=value&key=value form.

        Values are assumed to be encoded in the format specified by self._encoding,
        and are subsequently URL encoded.

        Args:
          post_data:
            A dict of (key, value) tuples, where value is encoded as
            specified by self._encoding

        Returns:
          A URL-encoded string in "key=value&key=value" form
        """
        if post_data is None:
            return None
        else:
            return urlencode(dict([(k, self._Encode(v))
                                   for k, v in list(post_data.items())]))

    def _RequestUrl(self, url, verb, data=None):
        """Request a url.

           Args:
             url:
               The web location we want to retrieve.
             verb:
               Either POST or GET.
             data:
               A dict of (str, unicode) key/value pairs.

           Returns:
             A JSON object.
        """
        if verb == 'POST':
            try:
                return requests.post(
                    url,
                    data=json.dumps(data),
                    headers={
                        'x-api-id': self._api_id,
                        'x-api-key': self._api_key,
                        'content-type': 'application/json'
                    }
                )
            except requests.RequestException as e:
                print('Error: ' + str(e))
        elif verb == 'GET':
            url = self._BuildUrl(url, extra_params=data)
            try:
                return requests.get(
                    url,
                    headers={
                        'x-api-id': self._api_id,
                        'x-api-key': self._api_key
                    }
                )
            except requests.RequestException as e:
                print('Error: ' + str(e))
        elif verb == 'PATCH':
            try:
                return requests.patch(
                    url,
                    data=json.dumps(data),
                    headers={
                        'x-api-id': self._api_id,
                        'x-api-key': self._api_key,
                        'content-type': 'application/json'
                    }
                )
            except requests.RequestException as e:
                print('Error: ' + str(e))
        elif verb == 'DELETE':
            url = self._BuildUrl(url, extra_params=data)
            try:
                return requests.delete(
                    url,
                    headers={
                        'x-api-id': self._api_id,
                        'x-api-key': self._api_key,
                        'content-type': 'application/json'
                    }
                )
            except requests.RequestException as e:
                print('Error: ' + str(e))

        return 0
