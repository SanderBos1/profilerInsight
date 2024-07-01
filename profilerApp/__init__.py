from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect 
import os
from cryptography.fernet import Fernet

db = SQLAlchemy()

#define the encrpyion keys:
key = os.getenv('ENCRYPTION_KEY')
cipher_suite = Fernet(key)

def create_app():


    app = Flask(__name__)

    databaseHost = os.getenv('databaseHost', 'localhost')  
    databasePort = os.getenv('databasePort', '5432') 
    databaseName= os.getenv('databaseName', 'test') 
    databaseUser = os.getenv('databaseUser', 'test')
    databasePassword = os.getenv('databasePassword', 'test')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{databaseUser}:{databasePassword}@{databaseHost}:{databasePort}/{databaseName}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"      
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY",)

    CSRFProtect (app)
    db.init_app(app)

    from .userConnections import databaseBP
    from .pages import htmlPagesBP
    from .userTables import usertableBP
    from .profiler import profilerBP

    app.register_blueprint(databaseBP)
    app.register_blueprint(htmlPagesBP)
    app.register_blueprint(usertableBP)
    app.register_blueprint(profilerBP)

    with app.app_context():
        # uncomment drop_all if you want to replace the database (when you have changed something)
        # db.drop_all()
        db.create_all()

    return app