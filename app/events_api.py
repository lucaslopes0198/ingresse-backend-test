import os
from flask import Flask, Blueprint, request, jsonify
from flask_marshmallow import Marshmallow
from schemas import ma, event_schema, events_schema
from database import app, db, Event, Tag, Datetime
from datetime import datetime

# Init Marshmallow
ma.init_app(app)

# Create a Event
@app.route('/events', methods=['POST'])
def add_event():
	name = request.json['name']
	place = request.json['place']
	interested = 0
	# datetimes = request.json['datetime']
	datetimes = [datetime(2015, 6, 5, 10, 20, 10, 10)]
	tags = request.json['tags']

	new_event = Event(name, place, interested)
	db.session.add(new_event)
	db.session.flush()
	db.session.refresh(new_event)

	new_datetimes = [Datetime(dt, new_event.id) for dt in datetimes] 
	new_tags = [Tag(t, new_event.id) for t in tags]

	db.session.bulk_save_objects(new_datetimes)
	db.session.bulk_save_objects(new_tags)
	db.session.commit()

	return event_schema.jsonify(new_event)

# Get All Events
@app.route('/events', methods=['GET'])
def fetch_all_events():
	all_events = Event.query.all()
	result = events_schema.dump(all_events)
	return jsonify(result)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
