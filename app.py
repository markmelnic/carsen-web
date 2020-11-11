from secrets import SECRET_KEY, SQLALCHEMY_DATABASE_URI

from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm

from mobile_de.methods import surface_search

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

@app.route("/")
def home():
    return redirect(url_for("doorway"))

@app.route("/doorway")
def doorway():
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template("doorway.html", register_form=register_form, login_form=login_form)

@app.route("/login", methods=["POST"])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()
    if login_form.validate_on_submit():
        return redirect(url_for("search"))
    else:
        return redirect(url_for("doorway"))
    #return render_template("doorway.html", register_form=register_form, login_form=login_form)

@app.route("/register", methods=["POST"])
def register():
    login_form = LoginForm()
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        return redirect(url_for("search"))
    else:
        return redirect(url_for("doorway"))
    #return render_template("doorway.html", register_form=register_form, login_form=login_form)

@app.route("/search", methods=["GET", "POST"])
def search():
    search_parameters = []
    search_parameters.append(request.form["car_make"])
    search_parameters.append(request.form["car_model"])
    for i in range(6):
        search_parameters.append("")
    data = surface_search(search_parameters)
    return render_template("search.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
