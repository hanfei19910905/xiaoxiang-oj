from flask_wtf import Form
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Regexp


class SubmitForm(Form):
    source = FileField('Source', validators=[FileAllowed(['zip', 'py'])])
    result = FileField('Result', validators=[FileAllowed(['csv', 'csv.zip'])])
    submit = SubmitField('Submit')