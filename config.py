from os import getenv
from datetime import timedelta


class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']


class DevelopmentConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@localhost/{}".format(
        getenv('DATABASE_USERNAME_DEV'),
        getenv('DATABASE_PASSWORD'),
        getenv('DATABASE_DEV')
    )

class DeploymentConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=10)
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        getenv('DATABASE_USERNAME'),
        getenv('DATABASE_PASSWORD'),
        getenv('DATABASE_HOST'),
        getenv('DATABASE_PORT'),
        getenv('DATABASE')
    )

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'deployment': DeploymentConfig
}
