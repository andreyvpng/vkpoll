from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SubmitField, HiddenField, \
    RadioField
from wtforms.validators import DataRequired


class CreatePollForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    options = FieldList(StringField())
    submit = SubmitField('Create')


class DeletePollForm(FlaskForm):
    poll_id = HiddenField()
    submit = SubmitField('Delete')


class VotePollForm(FlaskForm):
    poll_id = HiddenField()
    poll_url = HiddenField()
    options = RadioField()
    submit = SubmitField('Vote')
