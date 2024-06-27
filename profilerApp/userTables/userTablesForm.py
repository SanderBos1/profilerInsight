from flask_wtf import FlaskForm 
from wtforms import StringField
from wtforms.validators import DataRequired


class tableForm(FlaskForm):
    connectionId = StringField('Connection ID', validators=[DataRequired()])
    schema = StringField("Host", validators=[DataRequired()])
    table = StringField("Port", validators=[DataRequired()])
