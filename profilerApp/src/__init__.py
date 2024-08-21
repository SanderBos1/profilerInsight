import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from src.config import SingletonDB
from src.connectors import (
    connections_bp, db_profiler_bp, file_profiler_bp, 
    connection_tables_bp, errors_bp, data_quality_bp
)

def load_configuration(app, config_name):
    """
    Load environment variables and configure the app based on the environment.
    """
    env_files = {
        'development': '.env.development',
        'test': '.env.test',
        'production': '.env.production'
    }
    
    env_file = env_files.get(config_name, '.env')
    load_dotenv(env_file)

def configure_database(app, config_name):
    """
    Configure the database URI and initialize the database.
    """
    if config_name == 'test':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"postgresql://{os.getenv('databaseUser')}:{os.getenv('databasePassword')}@"
            f"{os.getenv('databaseHost')}:{os.getenv('databasePort')}/{os.getenv('databaseName')}"
        )
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def create_app(config_name=None):
    """
    Create and configure an instance of the Flask application.
    
    Args:
        config_name (str): The configuration environment name. Options are:
                           'development', 'test', or 'production'. Defaults to 'production'.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Load environment variables based on configuration
    load_configuration(app, config_name)
    
    # Register blueprints
    blueprints = [
        db_profiler_bp, file_profiler_bp, connections_bp,
        errors_bp, data_quality_bp, connection_tables_bp
    ]
    for bp in blueprints:
        app.register_blueprint(bp)
    
    # Configure Cross-Origin Resource Sharing (CORS)
    frontend_host = os.getenv("FRONTEND_HOST")
    frontend_port = os.getenv("FRONTEND_PORT")
    if frontend_host and frontend_port:
        cors_resources = {r"/*": {"origins": f"http://{frontend_host}:{frontend_port}"}}
        CORS(app, resources=cors_resources)
    
    # Configure database
    configure_database(app, config_name)
    
    # Configure session management
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    # Configure file upload settings
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app.config['csv_folder'] = os.path.join(base_dir, 'data', 'csvFiles')
    app.config['ALLOWED_EXTENSIONS'] = ['.xlsx', '.csv']

    # Initialize database
    db = SingletonDB.get_instance()
    db.init_app(app)
    
    # Create tables if not using in-memory SQLite (usually not needed for tests)
    if config_name != 'test':
        with app.app_context():
            db.create_all()

    return app
