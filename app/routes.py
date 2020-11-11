from mobile_de.scraper import next_page
from flask import request, render_template, url_for, redirect
from app import app, db, bcrypt
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def home():
    return redirect(url_for("doorway"))


@app.route("/doorway")
def doorway():
    if current_user.is_authenticated:
        return redirect(url_for("Dashboard"))
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template(
        "doorway.html", page="enter", title="Enter", register_form=register_form, login_form=login_form
    )


@app.route("/login", methods=["POST"])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("Dashboard"))
    return redirect(url_for("doorway"))


@app.route("/register", methods=["POST"])
def register():
    login_form = LoginForm()
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(login_form.password.data).decode("utf-8")
        user = User(name=register_form.name.data, email=register_form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("Dashboard"))
    else:
        return redirect(url_for("doorway"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def Dashboard():
    title = "Dashboard - " + str(current_user.name)
    return render_template("dashboard.html", page="dash", title=title)
