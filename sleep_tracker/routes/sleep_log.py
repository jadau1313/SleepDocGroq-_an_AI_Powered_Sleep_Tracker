from flask import Blueprint, render_template

sleep_log = Blueprint("sleep_log", __name__)

@sleep_log.route("/")
def log():
    return render_template("sleep_log.html")
