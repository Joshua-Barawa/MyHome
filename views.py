from flask import render_template, request, redirect, url_for, abort
from run import bcrypt
from run import db
from run import app
from run import mail
from models import *
from datetime import date
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm

from flask_mail import Message

from uuid import uuid1
import os
import requests, json

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def posts():
    posts = Post.query.all()
    message = ''
    if not posts:
        message = "You have not uploaded any blog"
    return render_template('blogs.html', posts=posts)


@app.route('/my-blogs')
def my_blogs():
    posts = Post.query.filter_by(owner=current_user.username)
    message = ''
    if not posts:
        message = "You have not uploaded any blog"
    return render_template('my_blogs.html', posts=posts)


@app.route('/post-form')
@login_required
def post_form():
    return render_template('post_form.html')


@app.route('/post-blog', methods=['POST'])
@login_required
def add_post():

    if request.method == 'POST':
        image = request.files['photo']
        location = request.form['location']
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        owner = current_user.full_names
        pic_filename = secure_filename(image.filename)
        pic_name = str(uuid1()) + "_" + pic_filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

        if location == '' or description == '' or title == '':
            return render_template("post_form.html", message="Please enter required fields")
        else:
            post = Post(image=pic_name, location=location, title=title, description=description, price=price, owner=owner)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("posts"))


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(register_form.password.data).decode('utf8')
        user = User(full_names=register_form.full_names.data, email=register_form.email.data, mobile_number=register_form.mobile_number.data, member_since=date.today(), password=password_hash)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=register_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, login_form.password.data):
                login_user(user)
                print(current_user)
                return redirect(url_for("posts"))
    return render_template('auth/login.html', form=login_form)


@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first()
    if user is None:
        abort(404)
    return render_template("profile.html", user=user)


@app.route('/blog/<int:id>')
@login_required
def read_more(id):
    blog = Blog.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(blog_id=id)
    if blog is None:
        abort(404)
    return render_template("readmore.html", blog=blog, comments=comments)


@app.route('/add-comment', methods=['POST'])
@login_required
def add_comment():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['comment']
        blog_id = request.form['blog_id'];
        if name == '' or description == '' :
            return render_template("readmore.html", message="Please enter required fields")
        else:
            comment = Comment(blog_id, name, description)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for("read_more", id=blog_id))


@app.route('/delete-comment/<int:id>')
@login_required
def delete_comment(id):
    delete_comment = Comment.query.filter_by(id=id).first()
    db.session.delete(delete_comment)
    db.session.commit()
    return redirect(url_for("read_more", id=delete_comment.blog_id))


@app.route('/blog-update/<int:id>')
@login_required
def blog_update_form(id):
    blog = Blog.query.filter_by(id=id).first()
    return render_template("blog_update.html", blog=blog)


@app.route('/update-blog/<int:id>', methods=['POST'])
@login_required
def blog_update(id):
    category = request.form['category']
    image = request.files['photo']
    heading = request.form['heading']
    description = request.form['description']
    posted = date.today()
    owner = current_user.username
    pic_filename = secure_filename(image.filename)
    pic_name = str(uuid1()) + "_" + pic_filename
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

    edited_blog = Blog.query.filter_by(id=id).update({"category_name":category, "image":pic_name, "heading":heading,
                                                       "description":description, "posted":posted, "owner":owner})

    db.session.commit()
    return redirect(url_for("my_blogs"))


@app.route('/delete-blog/<int:id>')
@login_required
def delete_blog(id):
    delete_blog = Blog.query.filter_by(id=id).first()
    db.session.delete(delete_blog)
    db.session.commit()
    return redirect(url_for("my_blogs"))


def send_mail(recipient):
    msg = Message(
        'Subscription',
        sender='mwamlandabarawa@gmail.com',
        recipients=[recipient]
    )
    msg.body = 'Hello, \n You have subscribed to our daily messaging.' \
               ' You will receive the best movie recommendations'
    mail.send(msg)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))