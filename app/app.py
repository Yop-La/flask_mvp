from flask import Flask
from flask_restful import Api
from blocklist import BLOCKLIST
from flask_jwt_extended import JWTManager
import os
from ma import ma
from models.user import UserModel
from commands.test_cmd import test_wd2

from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from db import db
from flask_migrate import Migrate


def create_app(conf=False):
    app = Flask(__name__)

    app.config.from_object('settings')

    api = Api(app)

    api = VideoRessource.add_enpoints(api)

    api = AggregateVideoRessource.add_enpoints(api)

    db.init_app(app)
    ma.init_app(ma)
    app.db = db

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        user = UserModel.find_by_id(identity)
        if user.is_admin:
            return {'is_admin': True}
        return {'is_admin': False}

    @app.route("/")
    def hello_world():
        return "<p>Hello, needl app data!</p>" + "<p>" + "</p>"


    api.add_resource(UserRegister, "/register", "/register/")
    api.add_resource(User, "/user/<int:user_id>")

    login_routes = [
        '/login',
    ]

    api.add_resource(UserLogin, *login_routes)

    refresh_routes = [
        '/refresh'
    ]

    api.add_resource(TokenRefresh, *refresh_routes)

    logout_routes = [
        '/logout'
    ]

    api.add_resource(UserLogout, *logout_routes)

    app.cli.add_command(test_wd2)

    migrate = Migrate(app, db)
    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
