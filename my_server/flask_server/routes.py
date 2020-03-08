from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_server import app, db, bcrypt
from flask_server.models import User, Post
from flask_server.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm, AddTagForm
from flask_server.server_functions import save_picture, code_picture, tags
from os import mkdir, chdir, getcwd 


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

        mkdir(getcwd() + "/flask_server/static/users" + "/" +
              str(User.query.filter_by(username=form.username.data).first().id))

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
    form1 = AddTagForm()
    if form.validate_on_submit():
        id = int(current_user.id)
        new_name = code_picture(form.picture_file.data)
        save_picture(form.picture_file.data, new_name, getcwd() + "/flask_server/static/users/" + str(id) + "/")

        post = Post(image_file=new_name, description=form.description.data,
                    tag_list=request.form.getlist('check'), user_id=current_user.id)
        db.session.add(post)
        db.session.commit()

        print(request.form.getlist('check'))
        print(current_user.posts)
    elif form1.validate_on_submit():
        user = User.query.filter_by(id=current_user.id)
        user.update({'user_tag_list': tags(form1.tags.data, current_user.user_tag_list)})
        db.session.commit()

        print(form1.tags.data)
        print(current_user.user_tag_list)
    return render_template("upload.html", title="Upload", form=form, form1=form1)
