from mobile_de.methods import surface_search
from json import loads
from flask import (
    request,
    render_template,
    url_for,
    redirect,
    flash,
    get_flashed_messages,
    jsonify,
)
from app import app, db, bcrypt
from app.forms import LoginForm, RegisterForm, SearchForm
from app.models import User, Favorite
from flask_login import login_user, current_user, logout_user, login_required

db.create_all()
db.session.commit()

def add_favorites(fav):
    find_dup = Favorite.query.filter_by(
        image=fav["image"],
        title=fav["title"],
        price=fav["price"],
        reg=fav["reg"],
        mileage=fav["mileage"],
    ).first()
    if find_dup != None:
        current_favs = current_user.favorites
        if not str(find_dup.id) in current_favs.split("|"):
            if current_favs == "":
                current_user.favorites = current_favs + str(find_dup.id)
            else:
                current_user.favorites = current_favs + "|" + str(find_dup.id)
            db.session.commit()
    else:
        fav_db = Favorite(
            url=fav["url"],
            image=fav["image"],
            title=fav["title"],
            price=fav["price"],
            reg=fav["reg"],
            mileage=fav["mileage"],
            user_added=current_user.id,
        )
        db.session.add(fav_db)
        db.session.flush()

        current_favs = current_user.favorites
        if current_favs == "":
            current_user.favorites = current_favs + str(fav_db.id)
        else:
            current_user.favorites = current_favs + "|" + str(fav_db.id)

        db.session.commit()

def get_favorites():
    if current_user.favorites == "":
        return ['']
    else:
        favorites = current_user.favorites.split("|")
        favs = []
        for i in favorites:
            fav = Favorite.query.get(i)
            favs.append([
                    fav.url,
                    fav.title,
                    fav.price,
                    fav.reg,
                    fav.mileage,
                    fav.image,
                ])

    return favs

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
        "doorway.html",
        page="enter",
        title="Enter",
        register_form=register_form,
        login_form=login_form,
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
            flash(u"Incorrect password - email combination!", "login_error")
            return redirect(url_for("doorway"))
    flash(u"User not found!", "login_error")
    return redirect(url_for("doorway"))


@app.route("/register", methods=["POST"])
def register():
    register_form = RegisterForm()
    login_form = RegisterForm()
    if register_form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(login_form.password.data).decode(
            "utf-8"
        )
        user = User(
            name=register_form.name.data,
            email=register_form.email.data,
            password=hashed_pass,
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("dashboard"))
    flash(u"Invalid credentials provided!", "register_error")
    return redirect(url_for("doorway"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    title = "Dashboard - " + str(current_user.name)
    favs = get_favorites()
    search_form = SearchForm()
    return render_template(
        "dashboard.html", page="dash", title=title, search_form=search_form, favs=favs
    )


@app.route("/search", methods=["POST"])
@login_required
def search():
    try:
        results = surface_search(
            [
                request.form["manufacturer"],
                request.form["model"],
                request.form["price_from"],
                request.form["price_to"],
                request.form["reg_from"],
                request.form["reg_to"],
                request.form["mileage_from"],
                request.form["mileage_to"],
            ]
        )
    except AssertionError:
        results = []
        flash(
            u"Your search did not yield any results. Try changing the parameters.",
            "no_search_results",
        )
    return render_template(
        "results.html",
        results=results,
    )


@app.route("/add_to_favorites", methods=["GET", "POST"])
@login_required
def add_to_favorites():
    fav = loads(request.form.to_dict()["qSet"])
    add_favorites(fav)

    favs = get_favorites()
    return render_template("favorites.html", favs=favs)
