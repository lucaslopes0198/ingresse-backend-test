import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Event Class/Model
class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	place = db.Column(db.String(100))
	interested = db.Column(db.Integer)
	datetimes = db.relationship('Datetime', backref='event', lazy=True)
	tags = db.relationship('Tag', backref='event', lazy=True)

	def __init__(self, name, place, interested):
		self.name = name
		self.place = place
		self.interested = interested

# Datetime Class/Model
class Datetime(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	datetime = db.Column(db.DateTime())
	event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

	def __init__(self, datetime, event_id):
		self.datetime = datetime
		self.event_id = event_id

# Tag Class/Model
class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tag = db.Column(db.String(100))
	event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

	def __init__(self, tag, event_id):
		self.tag = tag
		self.event_id = event_id