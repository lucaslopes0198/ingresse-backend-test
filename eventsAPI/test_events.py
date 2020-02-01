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
        self.test_dt = ["01/01/19 20:30:00", "02/01/19 22:00:00"]
        self.test_event = {'name': 'Test1 event', 'place': 'Test1 place', 'tags': ['Test1 t1', 'Test1 t2'], 'datetimes': self.test_dt}
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_event_creation(self):
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
        # Creating two events to have records
        self.test_event_creation()
        self.test_event_creation()
        response = self.client.get('/events')
        res_json = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_json), 2)
        self.assertEqual(len(res_json[0]), 6)
        self.assertEqual(len(res_json[1]), 6)

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
