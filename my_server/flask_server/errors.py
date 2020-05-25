from flask import render_template
from flask_server import db, app


@app.errorhandler(404)
def not_found_error(error):
    """
    Функция, отвечающая за работу с несуществующими страницами.

    :param error: код ошибки.
    :return: страница с кодом ошибки 404.
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Функция, работающая с ошибками связанными с сервером.

    :param error: код ошибки.
    :return: страница с кодом ошибки 500.
    """
    db.session.rollback()
    return render_template('500.html'), 500
