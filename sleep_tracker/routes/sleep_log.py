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
            awakenings=int(form.awakenings.data) if form.awakenings.data is not None else 0,   #wrap this in a try statement later for form validation
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
        return redirect(url_for('dashboard.view_dashboard'))
    return render_template('sleep_log.html', form=form)



@sleep_log.route("/sleep_logs")
@login_required
def sleep_logs():
    logs = SleepLog.query.filter_by(user_id=current_user.id).order_by(SleepLog.date)
    return render_template('sleep_logs.html', logs=logs)


@sleep_log.route("/edit_log.<int:log_id>", methods=["GET", "POST"])
@login_required
def edit_log(log_id):
    log = SleepLog.query.filter_by(id=log_id, user_id=current_user.id).first_or_404()
    form = SleepLogForm(obj=log)

    if form.validate_on_submit():
        log.date = form.date.data
        log.bedtime = form.bedtime.data
        log.risetime = form.risetime.data
        log.sleep_quality = form.sleep_quality.data
        log.relative_quality = form.relative_quality.data
        try:
            log.awakenings = int(form.awakenings.data) if form.awakenings.data is not None else 0
        except ValueError:
            flash("Invalid entry for awakenings", "danger")
            return render_template("edit_log.html", form=form, log=log)

        log.OSA_interventions = form.OSA_interventions.data
        log.caffeine = form.caffeine.data
        log.sleep_aid, log.alcohol, log.cannabis = form.sleep_aid.data, form.alcohol.data, form.cannabis.data
        log.typical_day = form.typical_day.data

        db.session.commit()
        flash("Edit success!", "success")
        return redirect(url_for("sleep_log.sleep_logs"))
    return render_template("edit_log.html", form=form, log=log)


@sleep_log.route("/delete/<int:log_id>", methods=["POST"])
@login_required
def delete_log(log_id):
    log = SleepLog.query.filter_by(id=log_id, user_id=current_user.id).first_or_404()
    db.session.delete(log)
    db.session.commit()
    flash("Sleep log successfully deleted", "success")
    return redirect(url_for("sleep_log.sleep_logs"))

