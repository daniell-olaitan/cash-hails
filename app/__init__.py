from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from config import config
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from models import db

jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_type: str) -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config[config_type])

    CORS(app, resources={
        r'/*': {
            'origins': '*'
        }
    })

    jwt.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        db.create_all()

    return app
