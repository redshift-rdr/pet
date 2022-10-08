from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, Email, EqualTo, ValidationError
from app.models import Engagement, EngagementTemplate, TasklistTemplate, Tasklist, Task, TaskTemplate

class AddEngagementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    client = StringField('Client')
    category = StringField('Category')
    start = DateField('Start date')
    end = DateField('End date')
    notes = TextAreaField('Notes')
    engagement_template = SelectField('Template')
    submit = SubmitField('Add')

    def __init__(self):
        super(AddEngagementForm, self).__init__()
        self.engagement_template.choices = [(et.uuid, et.title) for et in EngagementTemplate.query.all()]