from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from cryptography.fernet import Fernet
from flask_cors import CORS

db = SQLAlchemy()

#define the ecryption keys:
key = os.getenv('ENCRYPTION_KEY')
cipher_suite = Fernet(key)


def create_app():


    app = Flask(__name__)

    #allow vue frontend to communicate with the backend
    CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

    databaseHost = os.getenv('databaseHost')  
    databasePort = os.getenv('databasePort') 
    databaseName= os.getenv('databaseName') 
    databaseUser = os.getenv('databaseUser')
    databasePassword = os.getenv('databasePassword')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{databaseUser}:{databasePassword}@{databaseHost}:{databasePort}/{databaseName}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"      
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY",)

    #flat datasets are uploaded here
    base_dir =  os.path.dirname(os.path.abspath(__file__))
    app.config['csvFolder'] = os.path.join(base_dir, 'data', 'csvFiles')
    app.config['ALLOWED_EXTENSIONS'] = ['.xlsx', '.csv']

    db.init_app(app)

    from .userConnections import databaseBP
    from .userTables import usertableBP
    from .profiler import profilerBP
    from .csvProfiler import csvProfilerBP

    app.register_blueprint(databaseBP)
    app.register_blueprint(usertableBP)
    app.register_blueprint(profilerBP)
    app.register_blueprint(csvProfilerBP)

    with app.app_context():
        # uncomment drop_all if you want to replace the database (when you have changed something)
        # db.drop_all()
        db.create_all()

    return app