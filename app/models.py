from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

db.create_all()
db.session.commit()


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default="default.jpeg")
    password = db.Column(db.String(60), nullable=False)
    favorites = db.Column(db.String, default="")

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.profile_picture}')"


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    reg = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_added = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Vehicle('{self.url}', '{self.title}')"
