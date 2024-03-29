from flask import url_for
from flask_server import db, login_manager
from flask_login import UserMixin
from hashlib import md5


@login_manager.user_loader
def load_user(user_id):
    """
    Функция, обеспечивающая запоминание уже вошедших в аккаунт пользователей.

    :param user_id: идентификатор пользователя.
    :return: идентификатор пользователя из базы данных.
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_tag_list = db.Column(db.PickleType, default=["#Семья", "#Природа", "#Красота", "#Путешествие"])
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.id}', {self.username}', '{self.email}')"

    def set_user_photo(self):
        """
        Возвращает фотографию, созданную сервисом gravatar, если пользователь не выбирал фотографию,
        иначе возвращает выбранную им фотографию.

        :return: аватар пользователя.
        """

        if self.image_file == self.email:
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s=150'.format(digest)
        return url_for("static", filename="profile_pictures/" + self.image_file)

    def as_dict(self):
        """
        Функция, использющаяся при передаче данных пользователю.

        :return: словарь {*имя атрибута*: *атрибут*}.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tag_list = db.Column(db.PickleType, default=[])
    htwRatio = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.Text, nullable=False)
    hidden = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Post: '{self.id}', User: '{self.user_id}'"

    def as_dict(self):
        """
        Функция, использющаяся при передаче данных пользователю.

        :return: словарь {*имя атрибута*: *атрибут*}.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
