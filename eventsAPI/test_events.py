import unittest
import os
import json
from datetime import datetime

from app import db, create_app
from app import models

class EventTestCase(unittest.TestCase):
    def setUp(self):
        """Initialize app and define test variables."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.test_dt = ['01/01/19 20:30:00', '02/01/19 22:00:00']
        self.test_event = {'name': 'Test1 event', 'place': 'Test1 place', 'tags': ['Test1 t1', 'Test1 t2'], 'datetimes': self.test_dt}
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_event_create(self):
        """Test API can create an event."""
        response = self.client.post('/events',
                                    json=self.test_event)
        res_json = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_json), 6)
        self.assertEqual(len(res_json['datetimes']), 2)
        self.assertEqual(len(res_json['tags']), 2)

    def test_get_all_events(self):
        """Test API can get all events."""
        # Creating two events
        response = self.client.post('/events',
                                    json=self.test_event)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/events',
                                    json=self.test_event)
        self.assertEqual(response.status_code, 200)
        # Get all events
        response = self.client.get('/events')
        res_json = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_json), 2)
        self.assertEqual(len(res_json[0]), 6)
        self.assertEqual(len(res_json[1]), 6)

    def test_get_filtered_events(self):
        """Test API can get filtered events."""
        # Creating first event
        response = self.client.post('/events',
                                    json=self.test_event)
        self.assertEqual(response.status_code, 200)
        # Change tags, datetimes and creating a second event
        self.test_event['tags'] = ['Diff Tag1', 'Diff Tag2']
        self.test_event['datetimes'] = ['01/02/20 17:30:00', '02/02/20 19:00:00', '02/03/20 19:00:00']
        response = self.client.post('/events',
                                    json=self.test_event)
        self.assertEqual(response.status_code, 200)

        # Creating filters for first filtered search
        filters = {'name': 'Test1', 'datetimes': ['01/01/20 17:30:00', '01/02/20 17:30:00']}
        response = self.client.post('/events/filters',
                                    json=filters)
        res_json = json.loads(response.data)
        # Testing first filtered response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_json), 1)
        # Converting response and filter to datetime
        response_dt = [datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S') for dt in res_json[0]['datetimes']]
        filter_dt = [datetime.strptime(dt, '%d/%m/%y %H:%M:%S') for dt in filters['datetimes']]
        # Creating list of bool to testing
        dt_bool = [filter_dt[0] <= dt and filter_dt[1] >= dt for dt in response_dt]
        for res in res_json:
            self.assertEqual(len(res), 6)
            self.assertIn(True, dt_bool)
        
        # Creating filters for second filtered search
        filters = {'tags': ['Test1 t1']}
        response = self.client.post('/events/filters',
                                    json=filters)
        res_json = json.loads(response.data)
        # Testing second filtered response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_json), 1)
        for res in res_json:
            self.assertEqual(len(res), 6)

    def test_event_update(self):
        """Test API can update an existing event."""
        # Creating an event
        response = self.client.post('/events',
                                    json=self.test_event)
        self.assertEqual(response.status_code, 200)
        update = {'name': 'Name updated', 'tags': ['Tag1 updated', 'Tag2 updated'], 'datetimes': ['02/02/20 20:02:00', '04/02/20 23:30:00', '02/03/20 19:00:00']}
        # Updating name, tag and datetime
        response = self.client.put('/events/1',
                                   json=update)
        self.assertEqual(response.status_code, 200)
        # Get updated event
        response = self.client.get('/events')
        res_json = json.loads(response.data)
        self.assertEqual('Name updated', res_json[0]['name'])
        self.assertEqual(len(res_json[0]['tags']), 2)
        self.assertEqual(len(res_json[0]['datetimes']), 3)
        # Updating interested
        response = self.client.put('/events/1',
                                   json={'interested': True})
        self.assertEqual(response.status_code, 200)
        # Get updated event
        response = self.client.get('/events')
        res_json = json.loads(response.data)
        self.assertEqual(res_json[0]['interested'], 1)

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
