import os
from pathlib import Path
from flask import Flask, jsonify
from flask_smorest import Api
from blocklist import BLOCKLIST
# from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from resources.tag import blp as TagBlueprint
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.user import blp as UserBlueprint

# SQLAlchemy imports
from db import db # SQLAlchemy instance
import models

def create_app(db_url= None):
    # Put flask app in a method, so that you can easily create other instances, especially when testing.
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Store Rest API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger_ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["JWT_SECRET_KEY"] = "onis-key" # Key for signing JWT tokens
    # SQLAlchemy configs
    # "sqlite:///data.db" uri connects to the development sql db uri,
    # calls the environment variable  for storing secret values.
    # db_url or ... works like a trenary operator. If db_url is None, then the development sql db uri.
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", f"sqlite:///{Path(__file__).parent / 'data.db'}")
    # Path(__file__) shows the current file, then .parent shows its folder.
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #If true, would slow down sql
    
    from flask_migrate import Migrate

    db.init_app(app) # Initialises sql DB to flask app
    api = Api(app)
    migrate = Migrate(app, db) # Setup Albemic(flask_migrate).
    jwt = JWTManager(app) # Initialises flask jwt extended

    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        # Check if token is in blocked/ logout.
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.additional_claims_loader
    def add_jwt_claims(identity):
        if identity == 1: 
            # Identity is derived from the user.id
            # in the recieved jwt Token.
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "The token has expired",
                "error": "token_expired",
            }), 
            401,
        )

    @jwt.needs_fresh_token_loader
    def need_fresh_token(jwt_header, jwt_payload):
        # Error msg for endpoints needing a fresh token
        return (
            jsonify({
                "message": "Needs fresh token, reauthenticate",
                "error": "fresh_token_required",
            }), 401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        # error args is used on decorated function types
        # with no valid jwt payload/header from the client,
        # else a jwt_header & jwt_payload is used as seen above.
        return (
            jsonify({
                "message": "Signature verification failed",
                "error": "invalid_token",
            }), 
            401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
              "description" : "Request does not contain an access token.",
              "error" : "authorization_required"  
            }),
            401,
        )


    with app.app_context():
        db.create_all()
    # The code below is still a substitue for creatng tables
    # @app.before_request
    # def create_tables():
    #     db.create_all()


    api.register_blueprint(TagBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)
    return app
