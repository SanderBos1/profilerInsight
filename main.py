from flask import Flask
from flask_session import Session
from back_end import regression_bp

app = Flask(__name__)

app.register_blueprint(regression_bp)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)