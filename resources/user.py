from blocklist import BLOCKLIST
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity

from db import db
from models import UserModel
from flask import current_app
from tasks import send_user_registered_email
from schemas import UserSchema, UserRegisterSchema

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
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserRegisterSchema)
    def post(self, user_data):
        username = user_data["username"]
        email = user_data["email"]
        password = user_data["password"]
        # user = UserModel.query.get(username)
        
        from sqlalchemy import or_

        # or_ aids to checks if username or email exists
        if UserModel.query.filter(
            or_ (UserModel.username == username, UserModel.email == email)
            ).first():
            abort(409, message= "Username or email already exists")
        
        user = UserModel(
            username = username,
            email = email,
            password = pbkdf2_sha256.hash(password)
        )

        db.session.add(user)
        db.session.commit()

        
        send_user_registered_email(user.email, user.username) # WITHOUT QUEUE
        # current_app.queue.enqueue(send_user_registered_email, user.email, user.username)

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

