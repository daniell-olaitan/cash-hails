from flask import Blueprint


auth_views = Blueprint('auth', __name__, url_prefix='/auth')

from app.app_auth.views import *
