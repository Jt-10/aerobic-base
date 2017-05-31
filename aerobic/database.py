from . import db

class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False)
    activities = db.relationship("Activity", backref="athlete", lazy="dynamic")

    def __init__(self, access_token, name, activities):
        self.name = name
        self.access_token = access_token
        self.activities = activities

    def __repr__(self):
        return "<Name {}r>".format(self.name)

class Activity(db.Model):
    # Strava documentation on activity data at https://strava.github.io/api/v3/activities/
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Float)                        # 1 in meters
    moving_time = db.Column(db.Interval)                  # 2 in seconds
    total_elevation_gain = db.Column(db.Integer)          # 3 in meters
    type = db.Column(db.String)                           # 4 i.e. Run, Bike, Swim
    start_date = db.Column(db.Date)                       # 5 time string in GMT (i.e. 2012-12-13T03:43:19Z)
    start_date_local = db.Column(db.Date)                 # 6 time string in activity timezone
    average_speed = db.Column(db.Float)                   # 7 in meters per second
    average_heartrate = db.Column(db.Float)               # 8 average over moving portion
    aerobic_value = db.Column(db.Float)                   # 9 this is average_speed/average_heartrate
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'))

    def __init__(self, distance, moving_time, total_elevation_gain, type, start_date, start_date_local,
                 average_speed, average_heartrate, aerobic_value, athlete_id):
        self.distance = distance
        self.moving_time = moving_time
        self.total_elevation_gain = total_elevation_gain
        self.type = type
        self.start_date = start_date
        self.start_date_local = start_date_local
        self.average_speed = average_speed
        self.average_heartrate = average_heartrate
        self.aerobic_value = aerobic_value
        self.athlete_id = athlete_id

    def __repr__(self):
        return "<Athlete {}r>".format(self.athlete_id)

    def as_dictionary(self):
        activity = {
            "id": self.id,
            "distance": self.distance,
            "average_heartrate": self.average_heartrate,
            "average_speed": self.average_speed,
            "start_date": self.start_date,
            "aerobic_value": self.aerobic_value
        }
        return activity