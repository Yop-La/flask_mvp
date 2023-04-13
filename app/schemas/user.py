from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.user import UserModel


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password",)
        dump_only = ("id",)
        transient = True