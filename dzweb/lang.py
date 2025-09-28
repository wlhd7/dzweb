from flask import session, request, redirect, url_for
from flask_babel import Babel


def select_locale():
    return session.get('lang', 'zh')


def init_lang(app):
    Babel(app, locale_selector=select_locale)

    @app.post('/<string:lang>/set-lang')
    def set_lang(lang):
        session['lang'] = lang
        return redirect(request.args.get('next'))

