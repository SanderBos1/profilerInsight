from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, InputRequired, NumberRange
from flask_wtf.file import FileAllowed

class UploadForm(FlaskForm):
    headerRow = IntegerField('headerRow',  validators=[InputRequired(), NumberRange(min=0)])
    csvSeperator = SelectField('CSV Seperator', choices=[(',', 'Comma'), (';', 'Semicolon'), ('\t', 'Tab')], validators=[DataRequired()])
    quoteChar = SelectField('CSV Seperator', choices=[('"', '"')], validators=[DataRequired()])
    csvFile = FileField('Choose CSV File', validators=[DataRequired(), FileAllowed(['csv'], 'Only CSV files allowed!')])
    submit = SubmitField('Upload')