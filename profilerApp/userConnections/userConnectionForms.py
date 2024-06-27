from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class connectionForm(FlaskForm):
    connectionId = StringField('Connection ID', validators=[DataRequired()])
    host = StringField("Host", validators=[DataRequired()])
    port = StringField("Port", validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    database = StringField('Database', validators=[DataRequired()])
    submit = StringField('Submit', validators=[DataRequired()])