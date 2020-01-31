from app import ma

# Datetime Schema
class DatetimeSchema(ma.Schema):
	class Meta:
		fields = ['datetime']

# Tag Schema
class TagSchema(ma.Schema):
	class Meta:
		fields = ['tag']

# Event Schema
class EventSchema(ma.Schema):
	class Meta:
		fields = ['id', 'name', 'place', 'interested', 'tags', 'datetimes']
	tags = ma.Pluck(TagSchema, 'tag', many=True)
	datetimes = ma.Pluck(DatetimeSchema, 'datetime', many=True)

# Init schema
event_schema = EventSchema()
events_schema = EventSchema(many=True)
