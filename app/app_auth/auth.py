from models import db
from functools import wraps
from models.utils import Role
from models.models import User
from exc import AbortException
from flask_jwt_extended import jwt_required
from typing import (
    List,
    Tuple,
    Mapping,
    Callable
)
from flask import (
    abort,
    jsonify
)
from app import jwt
from models.models import InvalidToken
from flask.typing import ResponseReturnValue


@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(jwt_header: Mapping[str, str],
                                  jwt_payload: Mapping[str, str]) -> bool:
    """
    Check if user has logged out
    """
    jti = jwt_payload['jti']
    return InvalidToken.verify_jti(jti)


@jwt.expired_token_loader
def expired_token_callback(jwt_header: Mapping[str, str],
                           jwt_payload: Mapping[str, str]) -> ResponseReturnValue:
    """
    Check if access_token has expired
    """
    return jsonify({
        'status': 'fail',
        'data': {'token': 'token has expired'},
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header: Mapping[str, str],
                           jwt_payload: Mapping[str, str]) -> ResponseReturnValue:
    """
    Check if access_token has been revoked
    """
    return jsonify({
        'status': 'fail',
        'data': {'token': 'token has been revoked'},
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback(_) -> ResponseReturnValue:
    """
    Handle unauthorized access
    """
    return jsonify({
        'status': 'fail',
        'data': {'token': 'missing access token'},
    }), 401


class Auth:
    """
    Class for user authentication
    """
    @property
    def current_user(self) -> User:
        from flask_jwt_extended import get_jwt_identity

        user_id = get_jwt_identity()
        return db.get(User, id=user_id)

    def authenticate_user(self, phone: str, password: str) -> User:
        """
        Validate user login details
        """
        from app import bcrypt

        user = db.get(User, phone=phone)
        if user:
            if bcrypt.check_password_hash(user.password, password):
                return user

            raise AbortException({'error':'invalid password'})

        raise AbortException({'error':'phone not registerd'})

    def role_required(self, roles: List[Role] = [Role.ADMIN, Role.USER]) -> Callable:
        def decorator(f: Callable) -> Callable:
            @jwt_required()
            @wraps(f)
            def decorated_function(*args: Tuple, **kwargs: Mapping) -> ResponseReturnValue:
                if self.current_user.role not in roles:
                    abort(403)

                return f(*args, **kwargs)
            return decorated_function
        return decorator
