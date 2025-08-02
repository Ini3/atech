
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    # Register route blueprints
    from .routes.main import main
    from .routes.api import api
    from .routes.payments import payments
    from .routes.swagger import swagger

    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(payments)
    app.register_blueprint(swagger)

    return app
