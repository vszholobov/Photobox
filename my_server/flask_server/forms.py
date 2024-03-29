from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length
from flask_server.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(3, 15, message="Длина имени должна быть между 3 "
                                                                                      "и 15 символами")])
    email = StringField("Электронная почта", validators=[Email(), DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    confirm_password = PasswordField("Повтор пароля", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Отправить")

    @staticmethod
    def validate_username(_, username):
        """
        Функция проверки одинаковых имен пользователей при регистрации аккаунта.

        :param username: имя пользователя.
        :return: если пользователь уже существует, то ошибка, иначе - ничего.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Пользователь с таким именем уже существует.")

    @staticmethod
    def validate_email(_, email):
        """
        Функция проверки одинаковых email пользователей при регистрации аккаунта.

        :param email: email пользователя.
        :return: если email уже существует, то ошибка, иначе - ничего.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Пользователь с такой почтой уже существует.")


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(3, 15)])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class UpdateAccountForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(3, 15, message="Длина имени должна быть между 3 "
                                                                                      "и 15 символами")])
    email = StringField("Электронная почта", validators=[Email(), DataRequired()])
    picture = FileField("Изменить аватар", validators=[FileAllowed(["jpg", "png"])])
    password = PasswordField("Пароль", validators=[DataRequired()])
    confirm_password = PasswordField("Повтор пароля", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Обновить")

    @staticmethod
    def validate_username(_, username):
        """
        Функция проверки одинаковых имен пользователей при обновлении аккаунта.

        :param username: объект FlaskForm.
        :return: если пользователь уже существует, то ошибка, иначе - ничего.
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Пользователь с таким именем уже существует.")

    @staticmethod
    def validate_email(_, email):
        """
        Функция проверки одинаковых email пользователей при обновлении аккаунта.

        :param email: объект FlaskForm.
        :return: если email уже существует, то ошибка, иначе - ничего.
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Пользователь с такой почтой уже существует.")


class PostForm(FlaskForm):
    picture_file = MultipleFileField("Picture", validators=[DataRequired(), FileAllowed(["jpg", "png", "gif"])])
    description = TextAreaField("Description")
    submit = SubmitField("Отправить")
