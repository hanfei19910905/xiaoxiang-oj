from flask_wtf import Form
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class SubmitForm(Form):
    source = TextAreaField('Source', validators=[DataRequired()])
    submit = SubmitField('Submit')