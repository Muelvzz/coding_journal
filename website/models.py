from website import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    pass

class Post(db.Model):
    pass