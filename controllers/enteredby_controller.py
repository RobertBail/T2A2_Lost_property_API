#from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.enteredby import EnteredBy, enteredby_schema, enteredbys_schema
#from models.staff import Staff
#from controllers.auth_controller import auth_bp
from controllers.item_controller import item_bp
#from utils import authorise_as_admin

#enteredby_bp = Blueprint("claimedby", __name__, url_prefix="/<int:staff_id>/enteredby")
enteredby_bp = Blueprint("enteredby", __name__, url_prefix="/enteredby")
enteredby_bp.register_blueprint(item_bp) 

#needed? 
#def authorise_as_admin(fn):

@enteredby_bp.route('/')
def get_all_enteredbys():
    stmt = db.select(EnteredBy).order_by(EnteredBy.StaffName)
    enteredby = db.session.scalars(stmt)
    return enteredbys_schema.dump(enteredby)

@enteredby_bp.route('/<int:enteredby_id>')
def get_one_enteredby(enteredby_id):
    stmt = db.select(EnteredBy).filter_by(enteredby_id=enteredby_id)
    enteredby = db.session.scalar(stmt)
    if enteredby:
        return enteredby_schema.dump(enteredby)
    else:
        return {"error": f"Enteredby with id {enteredby_id} not found"}, 404

@enteredby_bp.route('/', methods=["POST"])
@jwt_required() 
def new_enteredby():
    body_data = enteredby_schema.load(request.get_json())
    # Create a new enteredby model instance
    enteredby = EnteredBy(
        StaffName = body_data.get('StaffName'),
        role = body_data.get('role'),
        staff_id=get_jwt_identity()
    )
    # Add that to the session and commit
    db.session.add(enteredby)
    db.session.commit()
    # return the newly created enteredby
    return enteredby_schema.dump(enteredby), 201

@enteredby_bp.route('/<int:enteredby_id>', methods=["DELETE"])
@jwt_required()
#@authorise_as_admin
def delete_enteredby(enteredby_id):

    stmt = db.select(EnteredBy).filter_by(enteredby_id=enteredby_id)
    enteredby = db.session.scalar(stmt)
    # if enteredby exists
    if enteredby:
#        is_admin = authorise_as_admin()
#        if not is_admin and str(enteredby.staff_id) != get_jwt_identity():    
        if str(enteredby.staff_id) != get_jwt_identity():
            return {"error": "Staff member is not authorised to perform this deletion."}, 403
        # delete the enteredby from the session and commit
        db.session.delete(enteredby)
        db.session.commit()
        # return msg
        return {'message': f"Enteredby '{enteredby.StaffName}' deleted successfully"}
    # else
    else:
        # return error msg
        return {'error': f"Enteredby with id {enteredby_id} not found"}, 404

@enteredby_bp.route('/<int:enteredby_id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_enteredby(enteredby_id):
    # Get the data to be updated from the body of the request
    body_data = enteredby_schema.load(request.get_json(), partial=True)
    # get the enteredby from the db whose fields need to be updated
    stmt = db.select(EnteredBy).filter_by(enteredby_id=enteredby_id)
    enteredby = db.session.scalar(stmt)
    # if enteredby exists
    if enteredby:
        if str(enteredby.staff_id) != get_jwt_identity():
            return {"error": "Only authorised staff members can edit these details"}, 403
        # update the fields
        enteredby.StaffName = body_data.get('StaffName') or enteredby.StaffName
        enteredby.role = body_data.get('role') or enteredby.role
        # commit the changes
        db.session.commit()
        # return the updated enteredby back
        return enteredby_schema.dump(enteredby)
    # else
    else:
        # return error msg
        return {'error': f'Enteredby with id {enteredby_id} not found'}, 404