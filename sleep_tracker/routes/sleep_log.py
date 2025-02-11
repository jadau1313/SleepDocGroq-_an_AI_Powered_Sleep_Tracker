from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, current_user
from sleep_tracker import db
from sleep_tracker.models import SleepLog
from forms import SleepLogForm
from datetime import datetime, date


sleep_log = Blueprint("sleep_log", __name__)
'''
@sleep_log.route("/")
def log():
    return render_template("sleep_log.html")
'''
@sleep_log.route('/', methods=['GET', 'POST'])
@login_required
def log_sleep():
    form = SleepLogForm()

    existing_entry = SleepLog.query.filter_by(user_id=current_user.id, date=date.today()).first() #need to modify this later

    if form.validate_on_submit():
        if existing_entry:
            flash("A log exists for this date")
            return redirect(url_for('edit_sleep_log', log_id = existing_entry.id))
        new_log = SleepLog(
            user_id=current_user.id,
            date=form.date.data,
            bedtime=form.bedtime.data,
            risetime=form.risetime.data,
            sleep_quality=form.sleep_quality.data,
            relative_quality=form.relative_quality.data,
            awakenings=form.awakenings.data,
            OSA_interventions=form.OSA_interventions.data,
            caffeine=form.caffeine.data,
            sleep_aid=form.sleep_aid.data,
            alcohol=form.alcohol.data,
            cannabis=form.cannabis.data,
            typical_day=form.typical_day.data

            ###left off here
        )
        new_log.calculate_sleep_period_duration()
        db.session.add(new_log)
        db.session.commit()
        flash("Log entry added. Success!", "success")
        return redirect(url_for('dashboard'))
    return render_template('sleep_log.html', form=form)