from app import db

# Event Class/Model
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    place = db.Column(db.String(100))
    interested = db.Column(db.Integer)
    datetimes = db.relationship('Datetime', backref='events', lazy=True)
    tags = db.relationship('Tag', backref='events', lazy=True)

    def __init__(self, name, place, interested):
        self.name = name
        self.place = place
        self.interested = interested

# Datetime Class/Model
class Datetime(db.Model):
    __tablename__ = 'datetimes'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime())
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __init__(self, datetime, event_id):
        self.datetime = datetime
        self.event_id = event_id

# Tag Class/Model
class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __init__(self, tag, event_id):
        self.tag = tag
        self.event_id = event_id
