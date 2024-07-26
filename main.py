import os

from flask import Flask
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from init import db, ma, bcrypt, jwt, migrate


def create_app():
    
    app = Flask(__name__)

    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app,db)

    @app.errorhandler(400)
    def bad_request(err):
        return {"error": str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {"error": str(err)}, 404

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return {"error": error.messages}, 400
    
    @app.errorhandler(401)
    def unauthenticated():
        return {"error": "You are not authenticated"}, 401

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)
# for staff

    from controllers.staffprofile_controller import staffprofile_bp
    app.register_blueprint(staffprofile_bp)

    from controllers.item_controller import item_bp
    app.register_blueprint(item_bp)

    from controllers.claimedby_controller import claimedby_bp
    app.register_blueprint(claimedby_bp)

    return app