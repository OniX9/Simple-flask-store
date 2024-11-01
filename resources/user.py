from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from blocklist import BLOCKLIST

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", __name__, "Operations on users")      


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        username = user_data["username"]
        password = user_data["password"]

        user = UserModel.query.filter(UserModel.username == username).first()

        if user and pbkdf2_sha256.verify(password, user.password):
            access_token = create_access_token(identity = user.id, fresh= True)
            refresh_token = create_refresh_token(identity = user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}


blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh= True)
    # The refreshToken is used to fetch new unfresh tokens,
    # unfresh tokens can't be used for important API calls.
    def post(self):
        user_id = get_jwt_identity
        new_token = create_access_token(identity= user_id, fresh= False)
        return {"access token": new_token}

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        username = user_data["username"]
        password = user_data["password"]
        # user = UserModel.query.get(username)
        
        if UserModel.query.filter(UserModel.username == username).first():
            abort(409, message= "Username already exists")
        
        user = UserModel(
            username = username,
            password = pbkdf2_sha256.hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return user  # Check if password is not returned based on the Schema
        # return {"message": "User created successfully."}, 201


@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti) # Adds token to be logged out.
        return {"message": "Successfully logged out."}

    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
        

    @jwt_required(fresh= True)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200

