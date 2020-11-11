from flask import request, render_template, url_for, redirect
from app import app
from app.forms import LoginForm, RegisterForm
from app.models import User


@app.route("/")
def home():
    return redirect(url_for("doorway"))


@app.route("/doorway")
def doorway():
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template(
        "doorway.html", register_form=register_form, login_form=login_form
    )


@app.route("/login", methods=["POST"])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()
    if login_form.validate_on_submit():
        return redirect(url_for("search"))
    else:
        return redirect(url_for("doorway"))
    # return render_template("doorway.html", register_form=register_form, login_form=login_form)


@app.route("/register", methods=["POST"])
def register():
    login_form = LoginForm()
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        return redirect(url_for("search"))
    else:
        return redirect(url_for("doorway"))
    # return render_template("doorway.html", register_form=register_form, login_form=login_form)


@app.route("/search", methods=["GET", "POST"])
def search():
    search_parameters = []
    search_parameters.append(request.form["car_make"])
    search_parameters.append(request.form["car_model"])
    for i in range(6):
        search_parameters.append("")
    data = surface_search(search_parameters)
    return render_template("search.html", data=data)
