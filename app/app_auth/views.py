from models import db
from typing import Dict
from models.models import (
    User,
    Admin,
    Profile
)
from flask import (
    abort,
    jsonify,
    request,
)
from models.utils import Role
from exc import AbortException
from pydantic import BaseModel
from models.validations import (
    UserRegSchema,
    AdminRegSchema,
    LoginSchema,
    ChangePwdSchema,
    validate_input,
    verify_json_input
)
from app.app_auth.auth import Auth
from app.app_auth import auth_views
from flask.typing import ResponseReturnValue
from flask_jwt_extended import create_access_token

auth = Auth()


def register_user(user_role: Role, user_details: Dict) -> None:
    if user_role == Role.ADMIN:
        if not validate_input(AdminRegSchema, **user_details):
            abort(422)

        model_type = Admin
        user_details['role'] = Role.ADMIN
    elif user_role == Role.USER:
        if not validate_input(UserRegSchema, **user_details):
            abort(422)

        model_type = Profile
        user_details['role'] = Role.USER

    if db.get(User, phone=user_details['phone']):
        raise AbortException({'error': 'phone already registered'}, 'Conflict', 409)

    user = db.save_new(User, **user_details)
    _ = db.save_new(model_type, user_id=user.id)
    return jsonify({
        'status': 'success',
        'data': user.to_dict()
    }), 201


@auth_views.route('/register', methods=['POST'])
@verify_json_input
def register() -> ResponseReturnValue:
    return register_user(Role.USER, request.json)


@auth_views.route('/register-admin', methods=['POST'])
@auth.role_required([Role.ADMIN])
@verify_json_input
def register_admin() -> ResponseReturnValue:
    return register_user(Role.ADMIN, request.json)


@auth_views.route('/login', methods=['POST'])
@verify_json_input
def login() -> ResponseReturnValue:
    if not validate_input(LoginSchema, **request.json):
        abort(422)

    user = auth.authenticate_user(request.json['phone'], request.json['password'])
    return jsonify({
        'status': 'success',
        'data': {
            'user': user.to_dict(),
            'access_token': create_access_token(user.id)
        }
    }), 200


@auth_views.route('/logout', methods=['GET'])
@auth.role_required()
def logout() -> ResponseReturnValue:
    from flask_jwt_extended import get_jwt
    from models.models import InvalidToken

    jti = get_jwt()['jti']
    db.save_new(InvalidToken, jti=jti)

    return jsonify({
        'status': 'success',
        'data': {}
    }), 200


@auth_views.route('/change-password', methods=['POST'])
@auth.role_required()
@verify_json_input
def change_password() -> ResponseReturnValue:
    if not validate_input(ChangePwdSchema, **request.json):
        abort(422)

    user = auth.authenticate_user(auth.current_user.phone, request.json['current_password'])
    user = db.update(User, id=user.id, password=request.json['new_password'])
    return jsonify({
        'status': 'success',
        'data': user.to_dict()
    }), 200
