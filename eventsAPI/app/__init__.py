from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name):
    from app.models import Event, Datetime, Tag
    from app.schemas import event_schema, events_schema

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)

    # Create a Event
    @app.route('/events', methods=['POST'])
    def add_event():
        name = request.json['name']
        place = request.json['place']
        interested = 0
        # datetimes = request.json['datetime']
        datetimes = [datetime(2015, 6, 5, 10, 20, 10, 10), datetime(2015, 6, 5, 10, 20, 10, 10)]
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

    return app
