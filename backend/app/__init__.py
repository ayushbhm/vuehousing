from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from routes.service_routes import service_bp
from routes.admin_routes import admin_bp
from routes.professional_routes import prof_bp
from routes.customer_routes import customer_bp
from routes.email_routes import email_bp
from config import Config
import redis

db = SQLAlchemy()

def create_app(config_class=Config):
    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)
    jwt = JWTManager(app)

    # Configuration
    app.config.from_object(config_class)
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

    # Initialize DB
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(service_bp, url_prefix='/service')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(prof_bp, url_prefix='/prof')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    app.register_blueprint(email_bp, url_prefix='/email')

    # Ensure DB tables are created
    with app.app_context():
        db.create_all()

    return app
