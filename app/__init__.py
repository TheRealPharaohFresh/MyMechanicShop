import os

from flask import Flask
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint

from .extensions import ma, limiter, cache
from .models import db
from .blueprints.customer import customers_bp
from .blueprints.service_ticket import service_tickets_bp
from .blueprints.mechanic import mechanics_bp
from .blueprints.inventory import inventory_bp


# Load environment variables from .env
load_dotenv()


SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'MyMechanicShop API'
    }
)


def create_app(config_name=None, testing=False):
    app = Flask(__name__)

    # Testing mode
    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Development / Production mode
    else:
        config_class = config_name or 'DevelopmentConfig'

        app.config.from_object(
            f'config.{config_class}'
        )

        database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')

        if not database_uri:
            raise RuntimeError(
                'SQLALCHEMY_DATABASE_URI is not set. '
                'Check your .env file or Render environment variables.'
            )

        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    # Initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # Register blueprints
    app.register_blueprint(
        customers_bp,
        url_prefix='/customers'
    )

    app.register_blueprint(
        service_tickets_bp,
        url_prefix='/service_tickets'
    )

    app.register_blueprint(
        mechanics_bp,
        url_prefix='/mechanics'
    )

    app.register_blueprint(
        inventory_bp,
        url_prefix='/inventory'
    )

    app.register_blueprint(
        swaggerui_blueprint,
        url_prefix=SWAGGER_URL
    )

    return app
