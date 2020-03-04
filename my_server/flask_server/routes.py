from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_server import app, db, bcrypt
from flask_server.models import User
from flask_server.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm
from flask_server.server_functions import save_picture


@app.route("/")
def home():
    return render_template("home.html", title="Homepage")


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        print(User.query.all())
        flash("Your account has been created! You are now able to log in")
        return redirect(url_for("login"))
    return render_template("register.html", form=form, title="Register")


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful.")
    return render_template("login.html", form=form, title="Login")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Аккаунт успешно обновлен!")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pictures/" + current_user.image_file)
    return render_template("account.html", form=form, image_file=image_file, title="Account")


@app.route("/search")
@login_required
def search():
    return render_template("search.html", title="Search")


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture_file:
            print(1)
        print(form.data)
        print(request.form.getlist('check'))
    return render_template("upload.html", title="Upload", form=form)
