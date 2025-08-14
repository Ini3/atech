
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    # Register route blueprints
    from.routes.client import client_bp
    from .routes.classes import classes_bp
    from .routes.sessions import sessions_bp
    from .routes.subscriptions import subscriptions_bp
    from .routes.swagger import swagger
    from .routes.scheduler import schedule_helper_bp
    from .routes.main import app

    app.register_blueprint(app)
    app.register_blueprint(client_bp)
    app.register_blueprint(classes_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(schedule_helper_bp)
    app.register_blueprint(subscriptions_bp)
    app.register_blueprint(swagger)

    return app
