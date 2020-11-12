from mobile_de.methods import surface_search
from flask import request, render_template, url_for, redirect, flash, get_flashed_messages, jsonify
from app import app, db, bcrypt
from app.forms import LoginForm, RegisterForm, SearchForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def home():
    return redirect(url_for("doorway"))


@app.route("/doorway")
def doorway():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template(
        "doorway.html", page="enter", title="Enter", register_form=register_form, login_form=login_form
    )


@app.route("/login", methods=["POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("dashboard"))
        else:
            flash(u'Incorrect password - email combination!', "login_error")
            return redirect(url_for("doorway"))
    flash(u'User not found!', "login_error")
    return redirect(url_for("doorway"))


@app.route("/register", methods=["POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(login_form.password.data).decode("utf-8")
        user = User(name=register_form.name.data, email=register_form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("dashboard"))
    flash(u'Invalid credentials provided!', "register_error")
    return redirect(url_for("doorway"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    title = "Dashboard - " + str(current_user.name)
    search_form = SearchForm()
    return render_template("dashboard.html", page="dash", title=title, search_form=search_form)

@app.route("/search", methods=["POST"])
@login_required
def search():
    title = "Dashboard - " + str(current_user.name)
    search_form = SearchForm()
    manufacturer = search_form.manufacturer.data
    model = search_form.model.data
    results = surface_search([manufacturer, model, '', '', '', '', '', ''])
    #return redirect(url_for("dashboard", results=results))
    return render_template("dashboard.html", page="dash", title=title, search_form=search_form, results=results)

