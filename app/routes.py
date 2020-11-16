from sqlalchemy.sql.schema import Index
from mobile_de.methods import surface_search, checker
from json import loads
from time import time
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
from app.models import User, Vehicle
from flask_login import login_user, current_user, logout_user, login_required

db.create_all()
db.session.commit()


def add_favorites(fav):
    find_dup = Vehicle.query.filter_by(
        image=fav["image"],
        title=fav["title"],
        price=fav["price"],
        reg=fav["reg"],
        mileage=fav["mileage"],
    ).first()
    current_favs = eval(current_user.favorites)
    if find_dup != None:
        if not find_dup.id in current_favs:
            current_favs[find_dup.id] = [change for change in eval(find_dup.changes)]
            current_user.favorites = str(current_favs)
            db.session.commit()
            return True
        else:
            return False
    else:
        fav_db = Vehicle(
            url=fav["url"],
            image=fav["image"],
            title=fav["title"],
            price=fav["price"],
            reg=fav["reg"],
            mileage=fav["mileage"],
            user_added=current_user.id,
            availability=True,
        )
        db.session.add(fav_db)
        db.session.flush()

        current_favs[fav_db.id] = []
        current_user.favorites = str(current_favs)

        db.session.commit()
        return True


def get_favorites(last=False):
    if current_user.favorites == r"{}":
        return [""]
    else:
        favs = []
        current_favs = eval(current_user.favorites)
        for item in current_favs:
            fav = Vehicle.query.get(item)
            favs.append(
                [
                    fav.url,
                    fav.title,
                    fav.price,
                    fav.reg,
                    fav.mileage,
                    fav.image,
                    fav.id,
                ]
            )

    return [favs[-1]] if last else favs


def find_changes():
    favorites = get_favorites()
    changes = [""]
    if not favorites[0] == "":
        try:
            changes, removed_items = checker(favorites)
            # change listing availability
            if not removed_items == []:
                for item in removed_items:
                    Vehicle.query.get(item).availability = False
                    db.session.commit()
            # index change to database
            if changes:
                for change in changes:
                    vehicle = Vehicle.query.get(change[6])
                    timestamp = str(int(time() * 1000000))
                    change_value = str(change[-1])
                    current_changes = eval(vehicle.changes)
                    try:
                        current_changes[list(current_changes.items())[-1][0] + 1] = {
                            "timestamp": timestamp,
                            "value": change_value,
                        }
                        vehicle.changes = str(current_changes)
                    except IndexError:
                        current_changes[0] = {
                            "timestamp": timestamp,
                            "value": change_value,
                        }
                        vehicle.changes = str(current_changes)
                    vehicle.price = int(change[2]) + int(change_value)
                    changes[changes.index(change)].append(
                        list(eval(vehicle.changes).items())[-1][0]
                    )
                    db.session.commit()
        except AssertionError:
            # no changes found
            pass
        finally:
            new_changes_urls = []
            if not changes[0] == "":
                new_changes_urls = [item[0] for item in changes]
            current_favs = eval(current_user.favorites)
            for item in current_favs:
                changed_vehicle = Vehicle.query.get(item)
                veh_changes = eval(Vehicle.query.get(item).changes)
                if (
                    len(list(veh_changes.items())) == 0
                    or changed_vehicle.url in new_changes_urls
                ):
                    continue
                if not list(veh_changes.items())[-1][0] in current_favs[item]:
                    last_change_id = list(veh_changes.items())[-1][0]
                    changed_by = int(veh_changes[last_change_id]["value"])
                    for change in veh_changes:
                        if not change in current_favs[item] and not change == last_change_id:
                            changed_by += int(veh_changes[change]["value"])
                            current_favs[item].append(change)
                    added_change = [
                        changed_vehicle.url,
                        changed_vehicle.title,
                        changed_vehicle.price - changed_by,
                        changed_vehicle.reg,
                        changed_vehicle.mileage,
                        changed_vehicle.image,
                        changed_vehicle.id,
                        changed_by,
                        last_change_id,
                    ]
                    try:
                        changes.remove("")
                    except ValueError:
                        pass
                    changes.append(added_change)
                    current_user.favorites = str(current_favs)
                    db.session.commit()

    return changes


def remove_favorite(id):
    current_favs = eval(current_user.favorites)
    del current_favs[int(id)]
    current_user.favorites = str(current_favs)
    db.session.commit()


def add_ignored_change():
    print()


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


@app.route("/load_favorites", methods=["POST"])
@login_required
def load_favorites():
    return render_template("favorites.html", favs=get_favorites())


@app.route("/add_to_favorites", methods=["POST"])
@login_required
def add_to_favorites():
    fav = loads(request.form.to_dict()["qSet"])
    status = add_favorites(fav)
    return (
        render_template("favorites.html", favs=get_favorites(last=True))
        if status
        else render_template("favorites.html", empty=True)
    )


@app.route("/remove_from_favorites", methods=["POST"])
@login_required
def remove_from_favorites():
    request_ = request.form.to_dict()["id"].split("-")[1]
    remove_favorite(request_)
    return "True"


@app.route("/check_changes", methods=["POST"])
@login_required
def check_changes():
    changes = find_changes()
    return render_template("changes.html", changes=changes)


@app.route("/update_favorites", methods=["POST"])
@login_required
def update_favorites():
    return render_template("favorites.html", favs=get_favorites())


@app.route("/ignore_change", methods=["POST"])
@login_required
def ignore_change():
    change_to_ignore = loads(request.form.to_dict()["qSet"])
    current_favs = eval(current_user.favorites)
    current_favs[int(change_to_ignore["item"])].append(
        int(change_to_ignore["change_id"])
    )
    current_user.favorites = str(current_favs)
    db.session.commit()
    return "True"
