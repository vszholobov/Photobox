from flask import render_template, url_for, redirect, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_server import app, db, bcrypt
from flask_server.models import User, Post
from flask_server.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm, AddTagForm
from flask_server.server_functions import save_picture, code_picture, tags, sort_pictures_by_tag, creation_date
from os import mkdir, getcwd, remove, path


@app.route("/ajax", methods=['GET', 'POST'])
def check():
    return jsonify([i.as_dict() for i in Post.query.all()])


@app.route("/bot", methods=['GET', 'POST'])
def bot_api():
    if request.method == "GET":
        return render_template("404.html")
    return jsonify(f"https://www.pythonanywhere.com/user/photobox/files/home/photobox/my_server/flask_server/static/users/10/images/37fa41a43d6976c0.jpg")


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

        mkdir(getcwd() + "/flask_server/static/users/" + str(user.id))
        mkdir(getcwd() + "/flask_server/static/users/" + str(user.id) + "/images/")

        print(f"(Зарегестрировался) ID: {user.id} | LOGIN: {user.username} | EMAIL: {user.email};")
        flash("Вы успешно зарегистрировались!")

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
            print(f"(Авторизировался) ID: {user.id} "
                  f"| LOGIN: {user.username} "
                  f"| EMAIL: {user.email};")
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Введенный вами Логин или Пароль неправильный!")
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
            # path = "static/profile_pictures"
            # path_file = path.join(app.root_path, path, current_user.image_file)
            # remove(path_file)

            new_name = code_picture(form.picture.data)
            picture_file = save_picture(form.picture.data, new_name)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash("Аккаунт успешно обновлен!")

        print(f"(Обновился) ID: {current_user.id} "
              f"| LOGIN: {current_user.username} "
              f"| EMAIL: {current_user.email} "
              f"| IMAGE: {current_user.image_file};")

        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename="profile_pictures/" + current_user.image_file)
    return render_template("account.html", form=form, image_file=image_file, title="Account")


@app.route("/search", methods=["POST", "GET"])
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

        print(f"(Загрузил) ID: {current_user.id} "
              f"| LOGIN: {current_user.username} "
              f"| EMAIL: {current_user.email};")

        for photo in form.picture_file.data:
            new_name = code_picture(photo)
            htwRatio = save_picture(photo, new_name, getcwd() + "/flask_server/static/users/" + str(id) + "/")

            post = Post(image_file=new_name, description=form.description.data,
                        tag_list=request.form.getlist('check'), user_id=current_user.id,
                        creation_date=creation_date(), htwRatio=htwRatio)

            print(f"~UPLOAD: {post.image_file};")

            db.session.add(post)
            db.session.commit()
    elif form1.validate_on_submit():
        user = User.query.filter_by(id=current_user.id)
        user.update({'user_tag_list': tags(form1.tags.data, current_user.user_tag_list)})
        db.session.commit()
    return render_template("upload.html", title="Upload", form=form, form1=form1)
