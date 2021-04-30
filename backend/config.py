import os

from dotenv import load_dotenv

import logging

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TOKEN_EXPIRATION = int(os.environ.get('TOKEN_EXPIRATION'))
    SCHEDULER_API_ENABLED = True

    @classmethod
    def init_app(cls, app):
        handler = logging.FileHandler(f'{basedir}/log/flask.log', encoding='UTF-8')
        handler.setLevel(logging.WARN)
        logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
        handler.setFormatter(logging_format)
        app.logger.addHandler(handler)


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @classmethod
    def init_app(cls, app):
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SCHEDULER_API_ENABLED = True
    TOKEN_EXPIRATION = int(os.environ.get('TOKEN_EXPIRATION'))

    @classmethod
    def init_app(cls, app):
        handler = logging.FileHandler(f'{basedir}/log/flask.log', encoding='UTF-8')
        handler.setLevel(logging.WARN)
        logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
        handler.setFormatter(logging_format)
        app.logger.addHandler(handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
