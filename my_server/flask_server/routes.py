from flask import render_template, url_for, redirect, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_server import app, db, bcrypt
from flask_server.models import User, Post
from flask_server.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm
from flask_server.server_functions import save_picture, code_picture, tags, sort_pictures_by_tag, creation_date
from os import mkdir, getcwd, remove, path
from random import randint
import shutil


@login_required
@app.route("/admin", methods=["GET", "POST"])
def admin():
    """
    Функция, проверяющая авторизацию администратора.

    :return: аккаунт администратора при удачной авторизации, иначе обновление страницы.
    """
    form = LoginForm()
    if request.method == "POST":
        if form.username.data == "1" and form.password.data == "2":
            return render_template("admin_panel.html", title="Admin")
    return render_template("admin.html", form=form, title="Admin")


@app.route("/ajax", methods=['GET', 'POST'])
def ajax():
    """
    Функция, обеспечивающая взаимодействие сервера с пользователями.

    :return: ответ на запрос со стороны пользователей.
    """
    result = None
    action = request.json["action"]

    if current_user.is_anonymous:
        return jsonify("Тебя заволжанили")

    if action == "init":
        result = [
            [i.as_dict() for i in Post.query.filter_by(hidden=False)] +
            [i.as_dict() for i in Post.query.filter_by(hidden=True, user_id=current_user.id)],
            [[i.as_dict()["username"], i.set_user_photo()] for i in User.query.all()],
            current_user.id
        ]
    elif action == "admin_init":
        result = [
            [user.as_dict() for user in User.query.all()],
            [i.set_user_photo() for i in User.query.all()]
        ]
    elif action == "adminGetUserPhotos":
        result = [i.as_dict() for i in Post.query.filter_by(user_id=request.json["user_id"])]
        print(result)
    elif action == "addTags":
        tag_string = request.json["tags"]
        user = User.query.filter_by(id=current_user.id)

        old_tag_list = current_user.user_tag_list.copy()
        user.update({'user_tag_list': tags(tag_string, current_user.user_tag_list)})
        db.session.commit()
        # Разница между текущими тегами и бывшими(добавленные теги)
        result = list(set(current_user.user_tag_list) - set(old_tag_list))
    elif action == "addTagsToImage":
        tag_string = request.json["tags"]
        image = Post.query.filter_by(id=request.json["imageId"])

        old_tag_list = image[0].tag_list
        image.update({"tag_list": tags(tag_string, image[0].tag_list)})
        db.session.commit()
        # Разница между текущими тегами и бывшими(добавленные теги)
        result = list(set(Post.query.filter_by(id=request.json["imageId"])[0].tag_list) - set(old_tag_list))
    elif action == "get_my_images":
        result = [i.as_dict() for i in Post.query.filter_by(user_id=current_user.id)]
    elif action == "changeImageHiddenAttr":
        hidden = request.json["hidden"]
        image = Post.query.filter_by(id=request.json["imageId"])
        image.update({"hidden": not hidden})
        db.session.commit()
    elif action == "changeDescription":
        image = Post.query.filter_by(id=request.json["imageId"])
        image.update({"description": request.json["description"]})
        db.session.commit()
    elif action == "deleteTagsImage":
        image = Post.query.filter_by(id=request.json["imageId"])
        tag_list = request.json["tags"]
        deleted_tags = []
        for tag in tag_list:
            new_tag_list = image[0].tag_list
            new_tag_list.pop(new_tag_list.index(tag))
            deleted_tags.append(tag)
            image.update({"tag_list": new_tag_list})
            db.session.commit()
        result = deleted_tags
    elif action == "adminDeleteUserPhoto":
        photo_id = request.json["photoId"]
        post_to_delete = Post.query.filter_by(id=int(photo_id)).first()
        static_path = "static/users"
        static_path += f"/{post_to_delete.user_id}/images"
        path_file = path.join(app.root_path, static_path, f"{post_to_delete.image_file}")
        try:
            remove(path_file)
        except OSError:
            print(f"~DELETION-ERROR: {path_file};")
        db.session.delete(post_to_delete)
        db.session.commit()
    elif action == "adminDeleteUser":
        user_id = request.json["userId"]
        print(user_id)
        user_to_delete = User.query.filter_by(id=int(user_id)).first()
        if user_to_delete.image_file != user_to_delete.email:
            static_path = "static/profile_pictures"
            path_file = path.join(app.root_path, static_path, user_to_delete.image_file)
            try:
                remove(path_file)
            except OSError:
                print(f"~DELETION-ERROR: {path_file};")
        user_posts = Post.query.filter_by(user_id=user_to_delete.id)
        for post in user_posts:
            db.session.delete(post)
        db.session.delete(user_to_delete)
        db.session.commit()
        static_path = "static/users"
        path_file = path.join(app.root_path, static_path, f"{user_to_delete.id}")
        try:
            shutil.rmtree(path_file)
        except OSError:
            print(f"~DELETION-ERROR: {path_file};")
    elif action == "userDeletePhoto":
        print(current_user.posts)
        post_to_delete = Post.query.filter_by(user_id=current_user.id, id=request.json["imageId"]).first()
        if post_to_delete is None:
            result = {"status": "error"}
        else:
            static_path = "static/users"
            static_path += f"/{post_to_delete.user_id}/images"
            path_file = path.join(app.root_path, static_path, f"{post_to_delete.image_file}")
            try:
                remove(path_file)
            except OSError:
                print(f"~DELETION-ERROR: {path_file};")

            db.session.delete(post_to_delete)
            db.session.commit()
            result = {"status": "success"}

    return jsonify(result)


@app.route("/bot", methods=['GET', 'POST'])
def bot_api():
    """
    Функция, обеспечивающая взаимодействие сервера с ботами.

    :return: ответ на запрос со стороны ботов.
    """
    if request.method == "GET":
        return render_template("404.html")

    action = request.json["action"]

    if action == "random":
        images = list(filter(lambda post: 'gif' not in post.image_file, list(Post.query.filter_by(hidden=False))))
        random_number = randint(0, len(images) - 1)
        random_image = images[random_number]
        return jsonify({"route": getcwd() + f"/flask_server/static/users"
                                            f"/{random_image.user_id}/images"
                                            f"/{random_image.image_file}"})
    if action == "tags":
        images = list(filter(lambda post: 'gif' not in post.image_file, list(Post.query.filter_by(hidden=False))))
        list_of_images = sort_pictures_by_tag(images, tags(request.json["tags"]))
        list_of_routes = []
        if len(list_of_images) < 1:
            return
        for i in range(len(list_of_images[0])):
            list_of_routes.append(getcwd() + f"/flask_server/static/users"
                                  f"/{list_of_images[1][i]}/images"
                                  f"/{list_of_images[0][i]}")
        return jsonify({"routes": list_of_routes})


@app.route("/")
def home():
    """
    Функция, перенаправлющая на главную страницу.

    :return: главная страница.
    """
    return render_template("home.html", title="Homepage")


@app.route("/register", methods=["POST", "GET"])
def register():
    """
    Функция, отвечающая за регистрацию пользователя.

    :return: страница логина, если уже зарегистрирован, иначе страница регистрации.
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    image_file=form.email.data)
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
    """
    Функция, отвечающая за авторизацию пользователя.

    :return: главная страница, если успешная авторизация, иначе страница авторицзации.
    """
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
    """
    Функция, отвечающая за выход из аккаунта и перенаправление на домашнюю страницу.

    :return: домашняя страница.
    """
    logout_user()
    return redirect(url_for("home"))


@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    """
    Функция, отвечающая за взаимодействие между пользователем и его аккаунтом.

    :return: обновленная страница аккаунта пользователя.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            if current_user.image_file != current_user.email:
                static_path = "static/profile_pictures"
                path_file = path.join(app.root_path, static_path, current_user.image_file)
                try:
                    remove(path_file)
                except OSError:
                    print(f"~DELETION-ERROR: {path_file};")
            new_name = code_picture(form.picture.data)
            picture_file = save_picture(form.picture.data, new_name)
            if not picture_file:
                pass
            else:
                current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
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
    """
    Функция, отвечающая за переадресацию на страницу поиска.

    :return: страница поиска.
    """
    return render_template("search.html", title="Search")


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    """
    Функция, отвечающая за загрузку фотографий на сервер.

    :return: страница загрузки фотографий.
    """
    form = PostForm()
    if form.validate_on_submit():
        id = int(current_user.id)

        print(f"(Загрузил) ID: {current_user.id} "
              f"| LOGIN: {current_user.username} "
              f"| EMAIL: {current_user.email};")

        for photo in form.picture_file.data:
            new_name = code_picture(photo)
            htwRatio = save_picture(photo, new_name, getcwd() + "/flask_server/static/users/" + str(id) + "/")
            if not htwRatio:
                print("Неправильное фото")
            else:
                post = Post(image_file=new_name, description=form.description.data,
                            tag_list=request.form.getlist('check'), user_id=current_user.id,
                            creation_date=creation_date(), htwRatio=htwRatio)

                print(f"~UPLOAD: {post.image_file};")

                db.session.add(post)
                db.session.commit()
    return render_template("upload.html", title="Upload", form=form)


@app.route("/my_images")
def my_images():
    """
    Функция, перенаправляющая на страницу фотографий пользователя.

    :return: страница фотографий пользователя.
    """
    return render_template("my_images.html", title="My images")
