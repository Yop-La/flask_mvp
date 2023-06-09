from flask_restful import Resource
from hmac import compare_digest
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
)

from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker, scoped_session

from models.user import UserModel
from schemas.user import UserSchema
from blocklist import BLOCKLIST
from flask_jwt_extended import jwt_required
from datetime import datetime
from flask import current_app as app


USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."



user_schema = UserSchema()

class UserRegister(Resource):
    @classmethod
    @jwt_required()
    def post(cls):

        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 400

        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201


class User(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):

        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        try:
            user_json = request.get_json()
            user_data = user_schema.load(user_json)
        except ValidationError as err:
            return err.messages, 400

        user = UserModel.find_by_username(user_data.username)

        if user and compare_digest(user_data.password, user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            expiration_date = datetime.now() + app.config["JWT_ACCESS_TOKEN_EXPIRES"]
            return {"access_token": access_token, "refresh_token": refresh_token,
                    "jwt_access_token_expires": expiration_date.timestamp() * 1000}, 200

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLOCKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(**{'user_id': user_id})}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        expiration_date = datetime.now() + app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        return {"access_token": new_token, "jwt_access_token_expires": expiration_date.timestamp() * 1000}, 200
