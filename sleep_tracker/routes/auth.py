from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sleep_tracker import db
from sleep_tracker.models import User
from forms import RegisterForm, LoginForm

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login Success!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid user or password!', 'danger')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfull   y!', 'info')
    return redirect(url_for('main.home'))

@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pwd = generate_password_hash(form.password.data, method='pbkdf2:sha256') #need to figure out what exactly this is
        #new_user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        new_user = User()
        new_user.username = form.username.data
        new_user.email = form.email.data
        new_user.password_hash = hashed_pwd
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template("register.html", form=form)
