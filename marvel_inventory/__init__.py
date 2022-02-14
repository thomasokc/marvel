#init is our apps directory. If something is not referenced here, our app won't know how to access it or if it exists

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from config import Config
from marvel_inventory.helpers import JSONEncoder
from .site.routes import site
from .api.routes import api
from .authentication.routes import auth
from .models import db as root_db, login_manager, ma


#A var we use so others parts of our app know to look here to access information
app = Flask(__name__)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

#Pulls info from our config and gets our app ready for it
app.config.from_object(Config)

root_db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.signin'
ma.init_app(app)
migrate = Migrate(app,root_db)

CORS(app)
app.json_encoder = JSONEncoder