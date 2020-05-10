from flask import render_template, url_for, redirect, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_server import app, db, bcrypt
from flask_server.models import User, Post
from flask_server.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm
from flask_server.server_functions import save_picture, code_picture, tags, sort_pictures_by_tag, creation_date
from os import mkdir, getcwd, remove, path
from random import randint
# import shutil


@app.route("/admin", methods=["GET", "POST"])
def admin():
    form = LoginForm()
    if request.method == "POST":
        if form.username.data == "1" and form.password.data == "2":
            return render_template("admin_panel.html", title="Admin")
    return render_template("admin.html", form=form, title="Admin")


@app.route("/ajax", methods=['GET', 'POST'])
def ajax():
    result = None
    action = request.json["action"]

    if not current_user:
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

    return jsonify(result)


@app.route("/bot", methods=['GET', 'POST'])
def bot_api():
    if request.method == "GET":
        return render_template("404.html")

    action = request.json["action"]

    if action == "random":
        images = Post.query.all()
        random_number = randint(0, len(images) - 1)
        random_image = images[random_number]
        return jsonify({"route": getcwd() + f"/flask_server/static/users"
                                            f"/{random_image.user_id}/images"
                                            f"/{random_image.image_file}"})
    if action == "tags":
        images = Post.query.filter_by(hidden=False)
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
    return render_template("home.html", title="Homepage")


@app.route("/register", methods=["POST", "GET"])
def register():
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
    return render_template("search.html", title="Search")


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
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
    return render_template("my_images.html", title="My images")


"""        
    post_to_delete = Post.query.filter_by(id=int(id))
    static_path = "static/users"
    static_path += f"/{post_to_delete[0].user_id}"
    path_file = path.join(app.root_path, static_path, f"{post_to_delete[0].image_file}")
    try:
        remove(path_file)
    except OSError:
        print(f"~DELETION-ERROR: {path_file};")
    db.session.delete(post_to_delete)
    db.session.commit()

    user_to_delete = User.query.filter_by(id=int(id))
    user_posts = Post.query.filter_by(user_id=user_to_delete[0].id)
    for post in user_posts:
        db.session.delete(post)
    db.session.commit()
    static_path = "static/users"
    path_file = path.join(app.root_path, static_path, f"{user_to_delete[0].id}") 
    try:
        shutil.rmtree(path_file)
    except OSError:
        print(f"~DELETION-ERROR: {path_file};")
"""
