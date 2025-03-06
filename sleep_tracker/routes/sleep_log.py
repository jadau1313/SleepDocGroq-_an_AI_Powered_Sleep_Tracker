from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, current_user
from fontTools.ttLib.woff2 import bboxFormat

from sleep_tracker import db
from sleep_tracker.ai_analysis import generate_sleep_insight
from sleep_tracker.models import SleepLog
from forms import SleepLogForm
from datetime import datetime, date
import matplotlib.pyplot as plt
import io
import base64



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
            #return redirect(url_for('edit_sleep_log', log_id = existing_entry.id))
            #return redirect(url_for('sleep_log.edit_log', log_id=existing_entry.id))

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

def dashboard(): #need to fix this still, having issues with the visuals getting saved and/or displayed. will address after ai insights completed. perhaps can use AI for visuals rather than matplotlib
    logs = SleepLog.query.filter_by(user_id=current_user.id).order_by(SleepLog.date.asc()).all()

    #grabs data from logs associated with current user id
    dates = [log.date for log in logs]
    sleep_durations = [log.sleep_period_duration for log in logs]
    sleep_quality = [log.sleep_quality for log in logs]
    awakenings = [log.awakenings for log in logs]

    #handle missing days: leave gaps for now

    #create plot
    #will need to clarify that this is really time in bed, not sleep time. For true accuracy, need to estimate WASO and subtract WASO from Time in Bed
    #issues with generating the image. will come back around to fix this after adding AI insights.
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(dates, sleep_durations, marker='o', linestyle='-', label="Sleep duration (hrs)")
    ax.set_title("Sleep duration over time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Hours slept")
    ax.legend() #what's this?

    #convert to base64 for html rendering
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    print("Generated image base64: ", graph_url[:100])

    return render_template("dashboard.html", graph_url=graph_url)

@sleep_log.route("/sleep_insights")
@login_required
def sleep_insights():
    logs = SleepLog.query.filter_by(user_id=current_user.id).all()
    if not logs:
        flash("No sleep data found")
        print("no sleep data found")
        return redirect(url_for('sleep_log.sleep_logs'))

    insights = {
        'average_duration': sum(log.sleep_period_duration/60 for log in logs) / len(logs),
        'common_bedtime': max(set([log.bedtime.strftime("%H:%M") for log in logs]), key=[log.bedtime.strftime("%H:%M") for log in logs].count),
        'average_awakenings': sum([log.awakenings for log in logs]) / len(logs),
        'best_day': max(logs, key=lambda x: x.sleep_quality).date,
        'best_quality': max(logs, key=lambda x: x.sleep_quality).sleep_quality,
        'worst_day': min(logs, key=lambda x: x.sleep_quality).date,
        'worst_quality': min(logs, key=lambda x: x.sleep_quality).sleep_quality,
        'alcohol_impact': 'Negative impact on sleep on alcohol days' if any(log.alcohol and (log.awakenings > 1 or log.relative_quality < 4 or log.sleep_quality < 4) for log in logs) else 'Minimal alcohol impact',
        'cannabis_impact': 'Improved quality of sleep on cannabis days' if any(log.cannabis and (log.sleep_quality > 4 or log.relative_quality > 4 or log.awakenings < 2) for log in logs) else 'Minimal or slightly negative cannabis impact',
        'sleep_aid_impact': 'Improved quality on sleep_aid days' if any(log.sleep_aid and log.sleep_quality > 4 or log.sleep_quality > 4 or log.awakenings < 2 for log in logs) else 'Minimal impact on sleep from sleep aids'


    }

    summary = generate_sleep_insight(insights)

    return render_template('sleep_insights.html', insights=insights, summary=summary)