import os
from flask import Flask, session

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'static/uploads'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = 'SECRET_KEY'

    @app.before_request
    def before_request_func():
        if not session.get('logged_in'):
            session['logged_in'] = False
            session['user'] = None

    @app.context_processor
    def inject_user():
        user = {
            "logged_in": session['logged_in'],
            "user_data": session['user']
        }
        return dict(user=user)

    router(app)
    return app


def router(app):

    from app.controllers import Home
    from app.controllers import Account
    # from app.views import Images

    app.register_blueprint(Home.bp)
    app.register_blueprint(Account.bp)
    # app.register_blueprint(images.bp)