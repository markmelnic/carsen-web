from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default="default.jpeg")
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.profile_picture}')"
