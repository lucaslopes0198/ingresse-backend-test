from flask import request, jsonify
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

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

    @app.route('/events', methods=['POST'])
    def add_event():
        name = request.json['name']
        place = request.json['place']
        interested = 0
        datetimes = [datetime.strptime(dt, '%d/%m/%y %H:%M:%S') for dt in request.json['datetimes']]
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

    @app.route('/events', methods=['GET'])
    def get_all_events():
        all_events = Event.query.all()
        result = events_schema.dump(all_events)
        return jsonify(result)

    @app.route('/events/filters', methods=['GET'])
    def get_filtered_events(**kwargs):
        search_name = "%{}%".format(request.json.get('name', ''))
        search_place = "%{}%".format(request.json.get('place', ''))
        search_tags = request.json.get('tags', '')
        search_dt = request.json.get('datetimes', '')
        query = Event.query\
            .join(Tag, Event.id==Tag.event_id)\
            .join(Datetime, Event.id==Datetime.event_id)\
            .filter(Event.name.like(search_name))\
            .filter(Event.place.like(search_place))
        if search_tags:
            query = query.filter(Tag.tag.in_(search_tags))
        if search_dt:
            converted_dt = [datetime.strptime(dt, '%d/%m/%y %H:%M:%S') for dt in search_dt]
            query = query.filter(Datetime.datetime.between(converted_dt[0], converted_dt[1]))
        filtered_events = query.all()
        result = events_schema.dump(filtered_events)
        return jsonify(result)

    @app.route('/events/<int:id>', methods=['PUT'])
    def update_event(id, **kwargs):
        event = Event.query.filter_by(id=id).first()
        
        if 'interested' in request.json:
            if request.json['interested']:
                event.interested += 1
            else:
                event.interested -= 1
            db.session.add(event)
            db.session.commit()
            result = event_schema.dump(event)
            return jsonify(result)

        name_update = request.json.get('name', '')
        place_update = request.json.get('place', '')
        tags_update = request.json.get('tags', '')
        dt_update = request.json.get('datetimes', '')

        if name_update:
            event.name = name_update
        if place_update:
            event.place = place_update
        db.session.add(event)

        if tags_update:
            Tag.query.filter_by(event_id=id).delete()
            tags_updated = [Tag(t, id) for t in tags_update]
            db.session.bulk_save_objects(tags_updated)

        if dt_update:
            Datetime.query.filter_by(event_id=id).delete()
            converted_dt = [datetime.strptime(dt, '%d/%m/%y %H:%M:%S') for dt in dt_update]
            dt_updated = [Datetime(dt, id) for dt in converted_dt]
            db.session.bulk_save_objects(dt_updated)

        db.session.commit()
        result = event_schema.dump(event)
        return jsonify(result)

    @app.route('/events/<int:id>', methods=['DELETE'])
    def delete_event(id):
        event = Event.query.filter_by(id=id).first()
        db.session.delete(event)
        db.session.commit()
        return {
            "msg": "event deleted successfully",
            "id": id 
        }

    return app
