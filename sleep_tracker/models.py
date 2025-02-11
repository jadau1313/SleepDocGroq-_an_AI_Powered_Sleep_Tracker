from flask_login import UserMixin, current_user
from datetime import datetime

from . import db



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class SleepLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False) #can't be unique as user could go to bed at 1am on 2/2 and again go to bed at 11pm on 2/2.
    bedtime = db.Column(db.Time, nullable=False)
    risetime = db.Column(db.Time, nullable=False)
    sleep_quality = db.Column(db.Integer, nullable=False) #1-5 score range, to be handled by the UI
    relative_quality = db.Column(db.Integer, nullable=False) #1-5 score range, to be handled by the UI
    awakenings = db.Column(db.Integer, nullable=False) #positive integer
    OSA_interventions = db.Column(db.Boolean, nullable=False)
    caffeine = db.Column(db.Boolean, nullable=False)
    sleep_aid = db.Column(db.Boolean, nullable=False)
    alcohol = db.Column(db.Boolean, nullable=False)
    cannabis = db.Column(db.Boolean, nullable=False)
    typical_day = db.Column(db.Boolean, nullable=False)
    sleep_period_duration = db.Column(db.Integer, nullable=False)

    def calculate_sleep_period_duration(self   ):
        today = datetime.combine(self.date, self.bedtime)
        tomorrow = datetime.combine(self.date, self.risetime)

        if self.risetime < self.bedtime:
            tomorrow = tomorrow.replace(day=self.date.day + 1)
        self.sleep_period_duration = int((tomorrow - today).total_seconds() / 60)
