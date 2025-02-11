from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.choices import RadioField
from wtforms.fields.datetime import DateField, TimeField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, email, EqualTo, Length, Email


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email  = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SleepLogForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    bedtime = TimeField('Bedtime', validators=[DataRequired()])
    risetime = TimeField('Rise Time', validators=[DataRequired()])
    sleep_quality = RadioField('Sleep Quality', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')] , validators=[DataRequired()])
    relative_quality = RadioField('Relative Sleep Quality compared to a typical night', choices=[(1, 'Much worse'), (2, 'Worse'), (3, 'Same'), (4, 'Better'), (5, 'Much Better')] , validators=[DataRequired()])
    awakenings = IntegerField('Number of times you remember waking up during the night', validators=[DataRequired()]) #need to ensure positive values only
    OSA_interventions = BooleanField('Did you use any interventions for OSA, or other sleep disorders? (ie CPAP/BPAP, Oral appliance, Inspire, etc...). If n/a, select no.')
    caffeine = BooleanField('Caffeine within 8 hours of bedtime?')
    sleep_aid = BooleanField('Sleep aid before bed?')
    alcohol = BooleanField('Alcohol today?')
    cannabis = BooleanField('Cannabis use today?')
    typical_day = BooleanField('Was today a typical day?')
    submit = SubmitField('Save Log')

