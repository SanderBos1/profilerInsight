from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class UploadForm(FlaskForm):
    csvFile = FileField('Choose CSV File', validators=[DataRequired(), FileAllowed(['csv'], 'Only CSV files allowed!')])
    submit = SubmitField('Upload')