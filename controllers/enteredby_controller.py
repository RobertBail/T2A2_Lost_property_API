from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.enteredby import EnteredBy, enteredby_schema, EnteredBySchema
from controllers.auth_controller import auth_bp
from utils import authorise_as_admin

enteredby_bp = Blueprint("enteredby", __name__, url_prefix="/enteredby")
enteredby_bp.register_blueprint(auth_bp) 
 
 
 
 

StaffName="Keith Smith",
            role="Admin Manager",
            #add anything else?