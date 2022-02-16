from flask import render_template, request, redirect, url_for, abort
from run import bcrypt
from run import db
from run import app
from models import *
from datetime import date
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm
from uuid import uuid1
import os


UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)


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


@app.route('/my-posts')
def my_posts():
    posts = Post.query.filter_by(owner=current_user.full_names)
    message = ''
    if not posts:
        message = "You have not uploaded any blog"
    return render_template('my_posts.html', posts=posts, message=message)


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
    user = User.query.filter_by(email=current_user.email).first()
    if user is None:
        abort(404)
    return render_template("profile.html", user=user)


@app.route('/post/<int:id>')
@login_required
def read_more(id):
    post = Post.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(post_id=id)
    if post is None:
        abort(404)
    if comments is None:
        message = "No comments"
    return render_template("readmore.html", post=post, comments=comments)


@app.route('/add-comment', methods=['POST'])
@login_required
def add_comment():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['comment']
        post_id = request.form['post_id'];
        if name == '' or description == '' :
            return render_template("readmore.html", message="Please enter required fields")
        else:
            comment = Comment(post_id, name, description)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for("read_more", id=post_id))


@app.route('/post-update/<int:id>')
@login_required
def post_update_form(id):
    post = Post.query.filter_by(id=id).first()
    return render_template("post_update.html", post=post)


@app.route('/update-post/<int:id>', methods=['POST'])
@login_required
def post_update(id):
    location = request.form['location']
    image = request.files['photo']
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    owner = current_user.full_names
    pic_filename = secure_filename(image.filename)
    pic_name = str(uuid1()) + "_" + pic_filename
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

    edited_post = Post.query.filter_by(id=id).update({"image":pic_name, "location":location, "title":title,
                                                       "description":description, "price":price, "owner":owner})

    db.session.commit()
    return redirect(url_for("my_posts"))


@app.route('/delete-post/<int:id>')
@login_required
def delete_blog(id):
    delete_post = Post.query.filter_by(id=id).first()
    db.session.delete(delete_post)
    db.session.commit()
    return redirect(url_for("my_posts"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))