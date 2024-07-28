#from datetime import date

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.staffprofile import StaffProfile, StaffProfileSchema, staffprofile_schema, staffprofiles_schema
#from utils import authorise_as_admin
staffprofile_bp = Blueprint("staffprofile", __name__, url_prefix="/staffprofile")

#needed? 
#def authorise_as_admin(fn):

@staffprofile_bp.route('/', methods=["GET"])
def get_all_staffprofiles():

    stmt = db.select(StaffProfile).order_by(StaffProfile.staff_name)
    staffprofile = db.session.scalars(stmt)
    return staffprofiles_schema.dump(staffprofile)

@staffprofile_bp.route('/<int:staffprofile_id>', methods=["GET"])
def get_one_staffprofile(staffprofile_id):
    stmt = db.select(StaffProfile).filter_by(staffprofile_id=staffprofile_id)
    staffprofile = db.session.scalar(stmt)
    if staffprofile:
        return staffprofile_schema.dump(staffprofile)
    else:
        return {"error": f"Staffprofile with id {staffprofile_id} not found"}, 404
                                               #change this id to just "id"?

@staffprofile_bp.route('/', methods=["POST"])
@jwt_required() 
def new_staffprofile():
    body_data = staffprofile_schema.load(request.get_json())
    # Create a new staffprofile model instance
    staffprofile = StaffProfile(
        staffprofile_id=get_jwt_identity(),
        staff_name = body_data.get("staff_name"),
        role = body_data.get("role"),
        staff_id=get_jwt_identity()
    )
    # Add that to the session and commit
    db.session.add(staffprofile)
    db.session.commit()
    # return the newly created staffprofile
    return staffprofile_schema.dump(staffprofile), 201

@staffprofile_bp.route('/<int:staffprofile_id>', methods=["DELETE"])
@jwt_required()
#@authorise_as_admin
def delete_staffprofile(staffprofile_id):

    stmt = db.select(StaffProfile).filter_by(staffprofile_id=staffprofile_id)
    staffprofile = db.session.scalar(stmt)
    # if staffprofile exists
    if staffprofile:
#        is_admin = authorise_as_admin()
#        if not is_admin and str(staffprofile.staff_id) != get_jwt_identity():    
        if str(staffprofile.staff_id) != get_jwt_identity():
            return {"error": "Staff member is not authorised to perform this deletion."}, 403
        # delete the staff profile from the session and commit
        db.session.delete(staffprofile)
        db.session.commit()
        # return msg
        return {'message': f"Staff Profile '{staffprofile.staff_name}' deleted successfully"}
    # else
    else:
        # return error msg
        return {'error': f"Staff Profile with id {staffprofile_id} not found"}, 404

@staffprofile_bp.route('/<int:staffprofile_id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_staffprofile(staffprofile_id):
    # Get the data to be updated from the body of the request
    body_data = staffprofile_schema.load(request.get_json(), partial=True)
    # get the staffprofile from the db whose fields need to be updated
    stmt = db.select(StaffProfile).filter_by(staffprofile_id=staffprofile_id)
    staffprofile = db.session.scalar(stmt)
    # if staffprofile exists
    if staffprofile:
        if str(staffprofile.staff_id) != get_jwt_identity():
            return {"error": "Only authorised staff members can edit these details"}, 403
        # update the fields
        staffprofile.staff_name = body_data.get("staff_name") or staffprofile.staff_name
        staffprofile.role = body_data.get("role") or staffprofile.role
        # commit the changes
        db.session.commit()
        # return the updated staffprofile back
        return staffprofile_schema.dump(staffprofile)
    # else
    else:
        # return error msg
        return {'error': f'Staff Profile with id {staffprofile_id} not found'}, 404