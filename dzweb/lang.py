from flask import session, request, redirect, url_for
from flask_babel import Babel, get_locale


def select_locale():
    lang = request.args.get('lang')
    if lang in ['zh', 'en', 'ja']:
        session['lang'] = lang
        return lang
    return session.get('lang', 'zh')


def init_lang(app):
    Babel(app, locale_selector=select_locale)
    
    # Inject get_locale to all templates
    @app.context_processor
    def inject_locale():
        return dict(get_locale=get_locale)

    @app.post('/<string:lang>/set-lang')
    def set_lang(lang):
        session['lang'] = lang
        return redirect(request.args.get('next'))

