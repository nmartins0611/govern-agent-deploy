"""Flask application factory"""

from flask import Flask
from flask_cors import CORS
from banking_app.database import init_db, seed_data
from banking_app.routes import api
import os


def create_app(config=None):
    """
    Create and configure the Flask application

    Args:
        config: Optional configuration dictionary

    Returns:
        Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    if config:
        app.config.update(config)

    # Enable CORS
    CORS(app)

    # Initialize database
    database_url = os.getenv('DATABASE_URL', 'sqlite:///banking.db')
    Session = init_db(database_url)

    # Seed database with sample data
    seed_data(Session)

    # Store session in app context
    @app.before_request
    def before_request():
        from flask import g
        g.db_session = Session()

    @app.teardown_request
    def teardown_request(exception=None):
        from flask import g
        session = getattr(g, 'db_session', None)
        if session is not None:
            session.close()

    # Make session available to routes
    app.db_session = Session()

    # Register blueprints
    app.register_blueprint(api)

    # Root endpoint
    @app.route('/')
    def index():
        return {
            "service": "Banking API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/api/v1/health",
                "balance": "/api/v1/accounts/<id>/balance",
                "transfer": "/api/v1/accounts/transfer",
                "transactions": "/api/v1/accounts/<id>/transactions"
            }
        }

    return app
