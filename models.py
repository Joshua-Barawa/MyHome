from run import db
from flask_login import UserMixin


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text)
    location = db.Column(db.String(255))
    title = db.Column(db.String(255))
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    owner = db.Column(db.String(255))

    def __init__(self, image, location, title,description, price, owner):
        self.image = image
        self.location = location
        self.title = title
        self.description = description
        self.price = price
        self.owner = owner


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_names = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    mobile_number = db.Column(db.Integer, nullable=False)
    member_since = db.Column(db.Date)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, full_names, email, mobile_number, member_since, password):
        self.full_names = full_names
        self.email = email
        self.mobile_number = mobile_number
        self.member_since = member_since
        self.password = password


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    name = db.Column(db.String(255))
    desc = db.Column(db.String(255))

    def __init__(self, post_id, name, desc):
        self.post_id = post_id
        self.name = name
        self.desc = desc
