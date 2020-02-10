# encoding: utf-8

import os
import time
import unittest
import statusio

API_ID = ''
API_KEY = ''
STATUSPAGE_ID = '568d8a3e3cada8c2490000dd'
COMPONENT = '568d8a3e3cada8c2490000ed'
CONTAINER = '568d8a3e3cada8c2490000ec'
COMPONENT_CONTAINER_COMBO = ['568d8a3e3cada8c2490000ed-568d8a3e3cada8c2490000ec']
METRIC_ID = '568d8ab5efe35d412f0006f8'

ID1 = ''
ID2 = ''


class ApiTest(unittest.TestCase):

    def setUp(self):
        self._api = statusio.Api(API_ID, API_KEY)

    # STATUS

    def testStatus1Summary(self):
        # Test the statusio.StatusSummary method
        print('Testing StatusSummary')
        data = self._api.StatusSummary(STATUSPAGE_ID)
        self.assertEqual(data['status']['error'], 'no')

    # SUBSCRIBER

    def testSubscriber1Add(self):
        # Test the statusio.SubscriberAdd method
        print('Testing SubscriberAdd')
        global ID1, ID2
        data = self._api.SubscriberAdd(
            STATUSPAGE_ID, "email", "test@example.com")
        self.assertEqual(data['status']['error'], 'no')
        ID1 = data['subscriber_id']
        print(data['subscriber_id'])
        print(ID1)

    def testSubscriber2List(self):
        # Test the statusio.SubscriberList method
        print('Testing SubscriberList')
        global ID1, ID2
        data = self._api.SubscriberList(STATUSPAGE_ID)
        self.assertEqual(data['status']['error'], 'no')
        self.assertEqual(data['result']['email'][0]['_id'], ID1)

    def testSubscriber3Update(self):
        # Test the statusio.SubscriberUpdate method
        print('Testing SubscriberUpdate')
        global ID1, ID2
        data = self._api.SubscriberUpdate(
            STATUSPAGE_ID, ID1, "test@example.com")
        self.assertEqual(data['status']['error'], 'no')

    def testSubscriber4Remove(self):
        # Test the statusio.SubscriberRemove method
        print('Testing SubscriberRemove')
        global ID1, ID2
        data = self._api.SubscriberRemove(STATUSPAGE_ID, ID1)
        self.assertEqual(data['status']['error'], 'no')

    # MAINTENANCE

    def testMaintenance1Schedule(self):
        # Test the statusio.MaintenanceSchedule method
        print('Testing MaintenanceSchedule')
        global ID1, ID2
        data = self._api.MaintenanceSchedule(
            STATUSPAGE_ID,
            COMPONENT_CONTAINER_COMBO,
            'Autotest',
            'Autotest Description',
            '2018/12/31',
            '23:59',
            '2019/01/01',
            '23:59')
        self.assertEqual(data['status']['error'], 'no')
        ID1 = data['result']

    def testMaintenance2List(self):
        # Test the statusio.MaintenanceList method
        print('Testing MaintenanceList')
        global ID1, ID2
        data = self._api.MaintenanceList(STATUSPAGE_ID)
        self.assertEqual(data['status']['error'], 'no')
        self.assertEqual(
            data['result']['upcoming_maintenances'][0]['_id'], ID1)
        ID2 = data['result']['upcoming_maintenances'][0]['messages'][0]['_id']

    def testMaintenance3Message(self):
        # Test the statusio.MaintenanceMessage method
        print('Testing MaintenanceMessage')
        global ID1, ID2
        data = self._api.MaintenanceMessage(STATUSPAGE_ID, ID2)
        self.assertEqual(data['status']['error'], 'no')

    def testMaintenance4Start(self):
        # Test the statusio.MaintenanceStart method
        print('Testing MaintenanceStart')
        global ID1, ID2
        data = self._api.MaintenanceStart(
            STATUSPAGE_ID, ID1, 'Autotest details')
        self.assertEqual(data['status']['error'], 'no')

    def testMaintenance5Update(self):
        # Test the statusio.MaintenanceUpdate method
        print('Testing MaintenanceUpdate')
        global ID1, ID2
        data = self._api.MaintenanceUpdate(
            STATUSPAGE_ID, ID1, 'Autotest details update')
        self.assertEqual(data['status']['error'], 'no')

    def testMaintenance7Finish(self):
        # Test the statusio.MaintenanceFinish method
        print('Testing MaintenanceFinish')
        global ID1, ID2
        data = self._api.MaintenanceFinish(
            STATUSPAGE_ID, ID1, 'Autotest details finish')
        self.assertEqual(data['status']['error'], 'no')

    def testMaintenance8Delete(self):
        # Test the statusio.MaintenanceDelete method
        print('Testing MaintenanceDelete')
        global ID1, ID2
        data = self._api.MaintenanceDelete(STATUSPAGE_ID, ID1)
        self.assertEqual(data['status']['error'], 'no')

    # INCIDENT

    def testIncident1Create(self):
        # Test the statusio.IncidentCreate method
        print('Testing IncidentCreate')
        global ID1, ID2
        data = self._api.IncidentCreate(
            STATUSPAGE_ID,
            COMPONENT_CONTAINER_COMBO,
            'Autotest',
            'Autotest details',
            300,
            100,
            'Example Notification Message Subject')
        self.assertEqual(data['status']['error'], 'no')
        ID1 = data['result']

    def testIncident2List(self):
        # Test the statusio.IncidentList method
        print('Testing IncidentList')
        global ID1, ID2
        data = self._api.IncidentList(STATUSPAGE_ID)
        self.assertEqual(data['status']['error'], 'no')
        self.assertEqual(data['result']['active_incidents'][0]['_id'], ID1)
        ID2 = data['result']['active_incidents'][0]['messages'][0]['_id']

    def testIncident3Message(self):
        # Test the statusio.IncidentMessage method
        print('Testing IncidentMessage')
        global ID1, ID2
        data = self._api.IncidentMessage(STATUSPAGE_ID, ID2)
        self.assertEqual(data['status']['error'], 'no')

    def testIncident5Update(self):
        # Test the statusio.IncidentUpdate method
        print('Testing IncidentUpdate')
        global ID1, ID2
        data = self._api.IncidentUpdate(
            STATUSPAGE_ID, ID1, 'Autotest details update', 300, 100, 'Example Notification Message Subject')
        self.assertEqual(data['status']['error'], 'no')

    def testIncident7Resolve(self):
        # Test the statusio.IncidentResolve method
        print('Testing IncidentResolve')
        global ID1, ID2
        data = self._api.IncidentResolve(
            STATUSPAGE_ID, ID1, 'Autotest details resolve', 300, 100, 'Example Notification Message Subject')
        self.assertEqual(data['status']['error'], 'no')

    def testIncident8Delete(self):
        # Test the statusio.IncidentDelete method
        print('Testing IncidentDelete')
        global ID1, ID2
        data = self._api.IncidentDelete(STATUSPAGE_ID, ID1)
        self.assertEqual(data['status']['error'], 'no')

    # METRIC

    def testMetric1Update(self):
        # Test the statusio.MetricUpdate method
        print('Testing MetricUpdate')
        global ID1, ID2
        data = self._api.MetricUpdate(STATUSPAGE_ID,
                                      METRIC_ID,
                                      20.69,
                                      1395981878000,
                                      ["2014-03-28T05:43:00+00:00",
                                       "2014-03-28T06:43:00+00:00",
                                       "2014-03-28T07:43:00+00:00",
                                       "2014-03-28T08:43:00+00:00",
                                       "2014-03-28T09:43:00+00:00",
                                       "2014-03-28T10:43:00+00:00",
                                       "2014-03-28T11:43:00+00:00",
                                       "2014-03-28T12:43:00+00:00",
                                       "2014-03-28T13:43:00+00:00",
                                       "2014-03-28T14:43:00+00:00",
                                       "2014-03-28T15:43:00+00:00",
                                       "2014-03-28T16:43:00+00:00",
                                       "2014-03-28T17:43:00+00:00",
                                       "2014-03-28T18:43:00+00:00",
                                       "2014-03-28T19:43:00+00:00",
                                       "2014-03-28T20:43:00+00:00",
                                       "2014-03-28T21:43:00+00:00",
                                       "2014-03-28T22:43:00+00:00",
                                       "2014-03-28T23:43:00+00:00",
                                       "2014-03-29T00:43:00+00:00",
                                       "2014-03-29T01:43:00+00:00",
                                       "2014-03-29T02:43:00+00:00",
                                       "2014-03-29T03:43:00+00:00"],
                                      [20.70,
                                       20.00,
                                       19.20,
                                       19.80,
                                       19.90,
                                       20.10,
                                       21.40,
                                       23.00,
                                       27.40,
                                       28.70,
                                       27.50,
                                       29.30,
                                       28.50,
                                       27.20,
                                       28.60,
                                       28.70,
                                       25.90,
                                       23.40,
                                       22.40,
                                       21.40,
                                       19.80,
                                       19.50,
                                       20.00],
                                      20.07,
                                      1395463478000,
                                      ["2014-03-22T04:43:00+00:00",
                                          "2014-03-23T04:43:00+00:00",
                                          "2014-03-24T04:43:00+00:00",
                                          "2014-03-25T04:43:00+00:00",
                                          "2014-03-26T04:43:00+00:00",
                                          "2014-03-27T04:43:00+00:00",
                                          "2014-03-28T04:43:00+00:00"],
                                      [23.10,
                                          22.10,
                                          22.20,
                                          22.30,
                                          22.10,
                                          18.70,
                                          17.00],
                                      10.63,
                                      1393476280000,
                                      ["2014-02-28T04:43:00+00:00",
                                          "2014-03-01T04:43:00+00:00",
                                          "2014-03-02T04:43:00+00:00",
                                          "2014-03-03T04:43:00+00:00",
                                          "2014-03-04T04:43:00+00:00",
                                          "2014-03-05T04:43:00+00:00",
                                          "2014-03-06T04:43:00+00:00",
                                          "2014-03-07T04:43:00+00:00",
                                          "2014-03-08T04:43:00+00:00",
                                          "2014-03-09T04:43:00+00:00",
                                          "2014-03-10T04:43:00+00:00",
                                          "2014-03-11T04:43:00+00:00",
                                          "2014-03-12T04:43:00+00:00",
                                          "2014-03-13T04:43:00+00:00",
                                          "2014-03-14T04:43:00+00:00",
                                          "2014-03-15T04:43:00+00:00",
                                          "2014-03-16T04:43:00+00:00",
                                          "2014-03-17T04:43:00+00:00",
                                          "2014-03-18T04:43:00+00:00",
                                          "2014-03-19T04:43:00+00:00",
                                          "2014-03-20T04:43:00+00:00",
                                          "2014-03-21T04:43:00+00:00",
                                          "2014-03-22T04:43:00+00:00",
                                          "2014-03-23T04:43:00+00:00",
                                          "2014-03-24T04:43:00+00:00",
                                          "2014-03-25T04:43:00+00:00",
                                          "2014-03-26T04:43:00+00:00",
                                          "2014-03-27T04:43:00+00:00",
                                          "2014-03-28T04:43:00+00:00"],
                                      [0.00,
                                          0.00,
                                          0.00,
                                          0.00,
                                          0.00,
                                          0.00,
                                          0.00,
                                          0.00,
                                          0.00,
                                          0.00,
                                          0.00,
                                          0.00,
                                          18.50,
                                          18.60,
                                          18.40,
                                          16.60,
                                          16.80,
                                          17.90,
                                          19.90,
                                          21.30,
                                          22.80,
                                          20.00,
                                          17.30,
                                          19.10,
                                          21.50,
                                          22.40,
                                          22.50,
                                          22.00,
                                          21.80])
        self.assertEqual(data['status']['error'], 'no')

    # COMPONENT

    def testComponent1List(self):
        # Test the statusio.ComponentList method
        print('Testing ComponentList')
        global ID1, ID2
        data = self._api.ComponentList(STATUSPAGE_ID)
        self.assertEqual(data['status']['error'], 'no')

    def testComponent2StatusUpdate(self):
        # Test the statusio.ComponentStatusUpdate method
        print('Testing ComponentStatusUpdate')
        global ID1, ID2
        data = self._api.ComponentStatusUpdate(
            STATUSPAGE_ID, COMPONENT, CONTAINER, 'Test status', 300)
        self.assertEqual(data['status']['error'], 'no')
