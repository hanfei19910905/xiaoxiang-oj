from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length


class SubmitForm(Form):
    source = FileField('Source', validators=[DataRequired()])
    result = FileField('Result', validators=[DataRequired()])
    submit = SubmitField('Submit')