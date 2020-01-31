import os
import sys
from flask import Flask
from app import db, create_app
from app import models

app = create_app(config_name=os.getenv('FLASK_ENV'))

with app.app_context():
    db.create_all()
