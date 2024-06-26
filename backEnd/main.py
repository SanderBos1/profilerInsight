from flask import Flask
from flask_migrate import Migrate
from database import databaseBP
from models.initializeDB import db
from pages import htmlPagesBP
import os

template_dir = os.path.abspath('../frontEnd/html')
static_dir = os.path.abspath('../frontEnd/static')
app = Flask('app',template_folder=template_dir, static_folder=static_dir)
app.register_blueprint(databaseBP)
app.register_blueprint(htmlPagesBP)


#connects to the database

databaseHost = os.getenv('databaseHost', 'localhost')  
databasePort = os.getenv('databasePort', '5432') 
databaseName= os.getenv('databaseName', 'test') 
databaseUser = os.getenv('databaseUser', 'test')
databasePassword = os.getenv('databasePassword', 'test')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{databaseUser}:{databasePassword}@{databaseHost}:{databasePort}/{databaseName}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# needed to correctly import the models
db.init_app(app)
from models import dbConncetions
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)
