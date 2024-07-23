from datetime import timedelta
import functools
import jsonpickle

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from init import bcrypt, db
from models.staff import Staff, StaffSchema, staff_schema, staffs_schema
from controllers.staffprofile_controller import staffprofile_bp
#from utils import auth_as_admin_decorator

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
auth_bp.register_blueprint(staffprofile_bp)
#change __name__ ?

@auth_bp.route("/register", methods=["POST"])
def register_staff():
    try:
        # get the data from the body of the request
        body_data = StaffSchema.load(request.get_json())

        # create an instance of the Staff model
        staff = Staff(
           organisation_name=body_data.get("organisation_name"),
           staff_email=body_data.get("staff_email")
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
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return jsonify ({"error": f"The column {err.orig.diag.column_name} is required"}), 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return jsonify ({"error": "Email address already in use"}), 409


@auth_bp.route("/login", methods=["POST"])
def login_staff():

    # Get the data from the request body
    body_data = StaffSchema.load(request.get_json())
    #body_data = staff_schema.load(request.get_json())

    # Find user with the email address
    # SELECT * FROM users WHERE email = 'user_email_here';
    stmt = db.select(Staff).filter_by(staff_email=body_data.get("staff_email"))
    staff = db.session.scalar(stmt)

    # If cannot find user account with email, return account not found error
    if staff and bcrypt.check_password_hash(
            staff.staff_password,
            body_data.get('staff_password')
            ):
        # create JWT token for user with expiry set for 7 days
        token = create_access_token(
            identity=str(staff.staff_id),
            expires_delta=timedelta(days=7)
            )
        # return user info with token as a JSON response
        return jsonify(
            {
            "staff_email": staff.staff_email,
            "token": token,
            "is_admin": staff.is_admin
            }
        ), 200
    # return an error and unauthorised status code
    # in the case of invalid fields
    else:
        return jsonify(
            {
                "Error": "Username or password is invalid"
            }
        ), 401


# Function to check if staff member is an admin (checking the is_admin field)
def is_staff_admin():

    # Get user_id from the JWT token
    staff_id = int(get_jwt_identity())

    # Find the user record with the user_id
    # SELECT * FROM users where user_id = jwt_user_id
    stmt = db.select(Staff).filter_by(staff_id=staff_id)
    staff = db.session.scalar(stmt)

    # For edge case where old JWT token is used for a deleted account
    if staff is None:
        return {
            "error": "The logged in staff member has been deleted. Please login again."
        }, 403

    # Return True if staff member is admin, otherwise False
    return staff.is_admin


# Decorator function to make sure staff member is an admin 
#def authorise_as_admin(fn):
#    @functools.wraps(fn)
#    def wrapper(*args, **kwargs):
        # Get staff_id from the JWT token
#        staff_id = get_jwt_identity()
    # fetch the user from the db
#        stmt = db.select(Staff).filter_by(staff_id=staff_id)
#        staff = db.session.scalar(stmt)
    # check whether the user is an admin or not
#        return staff.is_admin

#def auth_as_admin_decorator(fn):
def authorise_as_admin(fn):
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

    #Update staff here?
    #Delete staff here?
@auth_bp.route("/staff", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin
def update_staff():
    # get the fields from body of the request
    body_data = staff_schema.load(request.get_json(), partial=True)
    staff_password = body_data.get("staff_password")
    # add staff_email ?
    # fetch the staff member from the db
    stmt = db.select(Staff).filter_by(staff_id=get_jwt_identity())
    staff = db.session.scalar(stmt)
    # if staff member exists
    if staff:
        is_admin = authorise_as_admin()
        if not is_admin and str(staff.staff_id) != get_jwt_identity():
            return {"error": "Staff member is not authorised to perform this update."}, 403
        # update the fields
        # add staff_email or instead of organisation_name?
        staff.organisation_name = body_data.get("organisation_name") or staff.organisation_name
        staff.staff_email=body_data.get("staff_email") or staff.staff_email
        # user.password = <hashed-password> or user.password
        if staff_password:
            staff.staff_password = bcrypt.generate_password_hash(staff_password).decode("utf-8")
        # commit to the DB
        db.session.commit()
        # return a response
        return staff_schema.dump(staff)
    # else
    else:
        # return an error
        return {"error": "Staff member does not exist"}

# /auth/users/user_id - DELETE
@auth_bp.route("/staff/<int:staff_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_staff(staff_id):
    # find the staff member with the id from DB
    stmt = db.select(Staff).filter_by(staff_id=get_jwt_identity())
    staff = db.session.scalar(stmt)
    # if staff member exists
    if staff:
        is_admin = authorise_as_admin()
        if not is_admin and str(staff.staff_id) != get_jwt_identity():
            return {"error": "Staff member is not authorised to perform this deletion."}, 403
        # delete the user
        db.session.delete(staff)
        db.session.commit()
        # return a message
        return {"message": f"Staff member with id {staff_id} deleted"}
    # else
    else:
        # return error saying user does not exist
        return {"error": f"Staff member with id {staff_id} not found"}, 404



    #-- Deleting inactive users
    #DELETE FROM users
    #WHERE last_login_date < '2023-01-01';
    #https://www.nilebits.com/blog/2024/01/crud-in-sql/#1-creating-data-the-c-in-crud