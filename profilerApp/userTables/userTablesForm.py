from flask_wtf import FlaskForm 
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class tableForm(FlaskForm):
    uniqueTableName = StringField("uniqueTableName", validators=[DataRequired()])
    connectionId = SelectField('Connection ID', validators=[DataRequired()])
    schema = StringField("schema", validators=[DataRequired()])
    table = StringField("table", validators=[DataRequired()])
