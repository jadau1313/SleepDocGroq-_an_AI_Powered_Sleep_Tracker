from flask import Blueprint, render_template

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
def view_dashboard():
    return render_template("dashboard.html")