from datetime import timedelta
import functools
import jsonpickle

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from init import bcrypt, db
from models.staff import Staff, StaffSchema, staff_schema, staffs_schema
from controllers.staffprofile_controller import staffprofile_bp
#from utils import auth_as_admin_decorator

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register_staff():
    try:
        # get the data from the body of the request
        body_data = staff_schema.load(request.get_json())
        #partial=true
        # create an instance of the Staff model
        staff = Staff(
           organisation_name=body_data.get("organisation_name"),
           staff_email=body_data.get("staff_email"),
           
        )
        # extract the password from the body
        staff_password = body_data.get("staff_password")

        # hash the password
        if staff_password:
            staff.staff_password = bcrypt.generate_password_hash(staff_password).decode("utf-8")

        # add and commit to the DB
        db.session.add(staff)
        db.session.commit()
        #staff_schema = jsonpickle.encode(staff)
        # respond back
        return staff_schema.dump(staff), 201
    
    except ValidationError as ve:
        # Handle Marshmallow validation errors
        return {"error": ve.messages}, 400
        
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return jsonify ({"error": f"The column {err.orig.diag.column_name} is required"}), 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return jsonify ({"error": "Email address is already in use"}), 409
    except Exception as e:
        # Handle any other unexpected errors
        return {"error": str(e)}, 500


@auth_bp.route("/login", methods=["POST"])
def login_staff():
    body_data = staff_schema.load(request.get_json())
    
    print("Received JSON:", body_data)    
    # Query for staff member by email
    stmt = db.session.query(Staff).filter_by(staff_email=body_data.get("staff_email"))
    staff = db.session.scalar(stmt)
    if not request.data:
        return jsonify({"error": "Empty request body"}), 400

    if not staff:
        return {"error": "Invalid email. Staff member does not exist"}, 401

    # if given password does not match hashed password in database, return password error
    if not bcrypt.check_password_hash(
        staff.staff_password, body_data.get("staff_password")
    ):
        return {"error": "Password is incorrect"}, 401

    # Assuming account was found, create JWT
    token = create_access_token(
        identity=str(staff.staff_id), expires_delta=timedelta(days=3)
    )
    # Return the token along with the user info
    return jsonify({"staff_email": staff.staff_email, "token": token, "is_admin": staff.is_admin})

# Function to check if staff member is an admin (checking the is_admin field)
def is_staff_admin():

    # Get staff_id from the JWT token
    staff_id = int(get_jwt_identity())

    # Find the staff record with the staff_id
    # SELECT * FROM staff where staff_id = jwt_staff_id
    stmt = db.select(Staff).filter_by(staff_id=staff_id)
    staff = db.session.scalar(stmt)

    # For edge case where old JWT token is used for a deleted account
    if staff is None:
        return {
            "error": "The logged in staff member has been deleted. Please login again."
        }, 403

    # Return True if staff member is admin, otherwise False
    return staff.is_admin

#def auth_as_admin_decorator(fn):
def auth_as_admin_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # get the user's id from get_jwt_identity
        staff_id = int(get_jwt_identity())
        # fetch the entire user using the id
        stmt = db.select(Staff).filter_by(staff_id=staff_id)
        staff = db.session.scalar(stmt)
        # if user is an admin
        if staff is None:
            return {
                "error": "The logged in staff has been deleted. Please login again."
            }, 403

        if staff.is_admin:
            # allow the decorated function to execute
            return fn(*args, **kwargs)
        # else (user is not an admin)
        else:
            # return error
            return {"error": "Only admin can perform this action"}, 403

    return wrapper

@auth_bp.route("/", methods=["GET"]) 
def get_all_staff():
    stmt = db.select(Staff).order_by(Staff.staff_id)
    staff_members = db.session.scalars(stmt)
    return staffs_schema.dump(staff_members)
            
@auth_bp.route("/staff/<int:staff_id>")
def get_one_staff(staff_id):
    stmt = db.select(Staff).filter_by(staff_id=staff_id)
   
    staff_member = db.session.scalar(stmt)
    if staff_member:
        return staff_schema.dump(staff_member)
    else:
        return {"error": f"Staff member with id {staff_id} not found"}, 404


            #"/staff/<int:staff_id>"
@auth_bp.route("/staff/<int:staff_id>", methods=["PUT", "PATCH"])
@jwt_required()
#@authorise_as_admin
def update_staff(staff_id):
    # get the fields from body of the request
    body_data = staff_schema.load(request.get_json(), partial=True)
    password = body_data.get("password")
    # add staff_email ?
    # fetch the staff member from the db
    stmt = db.select(Staff).filter_by(staff_id=get_jwt_identity())
    staff = db.session.scalar(stmt)
    # if staff member exists
    if staff:
#        is_admin = authorise_as_admin(fn)
#        if not is_admin and str(staff.staff_id) != get_jwt_identity():
#            return {"error": "Staff member is not authorised to perform this update."}, 403
        # update the fields
        # add staff_email or instead of organisation_name?
        staff.organisation_name = body_data.get("organisation_name") or staff.organisation_name
        staff.staff_email=body_data.get("staff_email") or staff.staff_email
        # user.password = <hashed-password> or user.password
        if password:
            staff.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # commit to the DB
        db.session.commit()
        # return a response
        return staff_schema.dump(staff)
    # else
    else:
        # return an error
        return {"error": "Staff member does not exist"}


@auth_bp.route("/staff/<int:staff_id>", methods=["DELETE"])
@jwt_required()
#@auth_as_admin_decorator
def delete_staff(staff_id):
    # find the staff member with the id from DB
    stmt = db.select(Staff).filter_by(staff_id=get_jwt_identity())
    staff = db.session.scalar(stmt)
    # if staff member exists
    if staff:
#        is_admin = authorise_as_admin()
#        if not is_admin and str(staff.staff_id) != get_jwt_identity():
#            return {"error": "Staff member is not authorised to perform this deletion."}, 403
        # delete the staff member
        db.session.delete(staff)
        db.session.commit()
        # return a message
        return {"message": f"Staff member with id {staff_id} deleted"}
    # else
    else:
        # return error saying staff member does not exist
        return {"error": f"Staff member with id {staff_id} not found"}, 404



    #-- Deleting inactive users
    #DELETE FROM users
    #WHERE last_login_date < '2023-01-01';
    #https://www.nilebits.com/blog/2024/01/crud-in-sql/#1-creating-data-the-c-in-crud