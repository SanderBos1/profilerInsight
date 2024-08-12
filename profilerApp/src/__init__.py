from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flasgger import Swagger

db = SQLAlchemy()

def create_app(config_name=None):
    """
    Create and configure an instance of the Flask application.

    Args:
        config_name (str): The configuration environment name. 
                            Options are 'development', 'test', or None for production.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Load environment variables based on configuration
    if config_name == 'development':
        load_dotenv('.env.development')
    elif config_name == 'test':
        load_dotenv('.env.test')
    elif config_name == 'production':
        load_dotenv('.env.production')

    # Register blueprints
    from .connectors.connection_connector import connections_bp
    from .connectors.profiler_connector import db_profiler_bp
    from .connectors.file_connector import file_profiler_bp

    app.register_blueprint(db_profiler_bp)
    app.register_blueprint(file_profiler_bp)
    app.register_blueprint(connections_bp)

    # Register error handlers
    from .config.errors import register_error_handlers
    register_error_handlers(app)

    # Initialize Swagger for API documentation
    Swagger(app)

    # Configure Cross-Origin Resource Sharing (CORS)
    frontend_host = os.getenv("FRONTEND_HOST")
    frontend_port = os.getenv("FRONTEND_PORT")
    cors_resources = {r"/*": {"origins": f"http://{frontend_host}:{frontend_port}"}}
    CORS(app, resources=cors_resources)

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('databaseUser')}:{os.getenv('databasePassword')}@"
        f"{os.getenv('databaseHost')}:{os.getenv('databasePort')}/{os.getenv('databaseName')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configure session management
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    # Configure file upload settings
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app.config['csvFolder'] = os.path.join(base_dir, 'data', 'csvFiles')
    app.config['ALLOWED_EXTENSIONS'] = ['.xlsx', '.csv']

    # Initialize database and create tables
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app
