from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    config_name = config_name or os.getenv('FLASK_ENV', 'default')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    # Register route blueprints
    from app.routes.client import client_bp
    from app.routes.classes import classes_bp
    from app.routes.sessions import sessions_bp
    from app.routes.subscriptions import subscriptions_bp
    from app.routes.swagger import swagger
    from app.routes.scheduler import schedule_helper_bp
    from app.routes.main import app as main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(classes_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(schedule_helper_bp)
    app.register_blueprint(subscriptions_bp)
    app.register_blueprint(swagger)

    return app
