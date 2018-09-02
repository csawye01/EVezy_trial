import os
basedir = os.path.abspath(os.path.dirname(__file__))


class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SSL_DISABLE = True

    @staticmethod
    def init_app(app):
        pass
