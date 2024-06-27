from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app():


    app = Flask(__name__)

    databaseHost = os.getenv('databaseHost', 'localhost')  
    databasePort = os.getenv('databasePort', '5432') 
    databaseName= os.getenv('databaseName', 'test') 
    databaseUser = os.getenv('databaseUser', 'test')
    databasePassword = os.getenv('databasePassword', 'test')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{databaseUser}:{databasePassword}@{databaseHost}:{databasePort}/{databaseName}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False      
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY",)

    db.init_app(app)

    from .userConnections import databaseBP
    from .pages import htmlPagesBP
    from .userTables import usertableBP

    app.register_blueprint(databaseBP)
    app.register_blueprint(htmlPagesBP)
    app.register_blueprint(usertableBP)

    with app.app_context():
        # uncomment drop_all if you want to replace the database (when you have changed something)
        # db.drop_all()
        db.create_all()

    return app