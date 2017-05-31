import unittest
import os

import sys; print(list(sys.modules.keys()))

# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from aerobic import app, db, Athlete, Activity

test_response = [
    {"start_date_local": "2015-09-15T19:48:14Z", "average_speed": 2.0,
     "has_heartrate": False, "average_heartrate": 156.0},
    {"start_date_local": "2015-10-01T19:48:14Z", "average_speed": 2.0,
     "has_heartrate": True, "average_heartrate": 154.0},
    {"start_date_local": "2015-12-15T19:48:14Z", "average_speed": 2.0,
     "has_heartrate": True, "average_heartrate": 152.0},
    {"start_date_local": "2016-03-01T19:48:14Z", "average_speed": 2.0,
     "has_heartrate": True, "average_heartrate": 150.0},
    {"start_date_local": "2016-05-15T19:48:14Z", "average_speed": 2.1,
     "has_heartrate": True, "average_heartrate": 148.0},
    {"start_date_local": "2016-08-01T19:48:14Z", "average_speed": 2.1,
     "has_heartrate": True, "average_heartrate": 146.0},
    {"start_date_local": "2016-10-15T19:48:14Z", "average_speed": 2.1,
     "has_heartrate": True, "average_heartrate": 144.0},
    {"start_date_local": "2017-01-01T19:48:14Z", "average_speed": 2.2,
     "has_heartrate": True, "average_heartrate": 142.0},
    {"start_date_local": "2017-03-15T19:48:14Z", "average_speed": 2.2,
     "has_heartrate": True, "average_heartrate": 140.0},
    {"start_date_local": "2017-04-01T19:48:14Z", "average_speed": 2.3,
     "has_heartrate": True, "average_heartrate": 138.0},
    {"start_date_local": "2017-05-15T19:48:14Z", "average_speed": 2.4,
     "has_heartrate": True, "average_heartrate": 136.0},
]

class TestAPI(unittest.TestCase):
    """ Tests for the aerobic API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        db.create_all()


    def tearDown(self):
        """ Test teardown """
        db.close()
        # Remove the tables and their data from the database
        db.drop_all()
