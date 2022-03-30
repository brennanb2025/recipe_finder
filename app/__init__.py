from flask import Flask
import os
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
#from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config.from_object(Config)

#csrf protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
csrf.init_app(app)

#url_for in javascript
from flask_jsglue import JSGlue
jsglue = JSGlue(app)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
#database
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True) #because sqlite can't alter without this

from app import routes
#from app.CsrfDb import models
