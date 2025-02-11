import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST
import models

from resources.item import blp as itemBliueprint
from resources.store import blp as storeBlueprint
from resources.tag import blp as tagBlueprint
from resources.user import blp as userBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Store REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = secrets.token_hex(32)
    jwt = JWTManager(app)

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"description": "Token has been revoked", "error": "token_revoked"}),   
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in BLOCKLIST


    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        # Look in the database for the user and see if they are an admin
        # This identity corresponds to the User id
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"description": "Token has expired", "error": "token_expired"}),
            401,
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"description": "Signature verification failed", "error": "invalid_token"}),
            401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"description": "Request does not contain an access token", "error": "authorization_required"}),
            401,
        )

    # This is deprecated
    # @app.before_first+request
    # def create_tables():
    #     db.create_all()

    with app.app_context():
        db.create_all()

    api.register_blueprint(itemBliueprint)
    api.register_blueprint(storeBlueprint)
    api.register_blueprint(tagBlueprint)
    api.register_blueprint(userBlueprint)

    return app
