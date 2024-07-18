from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from init import bcrypt, db
from models.staff import Staff, staff_schema, staffs_schema
#from controllers.enteredby_controller import enteredby_bp
from utils import auth_as_admin_decorator

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
#auth_bp.register_blueprint(enteredby_bp)
#change __name__ ?

@auth_bp.route("/register", methods=["POST"])
def register_staff():
    try:
        # get the data from the body of the request
        body_data = staff_schema.load(request.get_json())

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

        # respond back
        return staff_schema.dump(staff), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409


@auth_bp.route("/login", methods=["POST"])
def login_staff():

    # Get the data from the request body
    body_data = staff_schema.load(request.get_json())

    # Find user with the email address
    # SELECT * FROM users WHERE email = 'user_email_here';
    stmt = db.select(Staff).filter_by(staff_email=body_data.get("staff_email"))
    staff = db.session.scalar(stmt)

    # If cannot find user account with email, return account not found error
    if not staff:
        return {"error": "Invalid email. Staff member email does not exist"}, 401

    # if given password does not match hashed password in database, return password error
    if not bcrypt.check_password_hash(
        staff.staff_password, body_data.get("staff_password")
    ):
        return {"error": "Password is incorrect"}, 401

    # Assuming account was found, create JWT
    token = create_access_token(
        identity=str(staff.staff_id), expires_delta=timedelta(days=1)
    )
    # Return the token along with the user info
    return {"staff_email": staff.staff_email, "token": token, "is_admin": staff.is_admin}


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


# Decorator function to make sure staff member is an admin (for games, platforms and genre routes)
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        # Get user_id from the JWT token
        staff_id = int(get_jwt_identity())

        # SELECT * FROM users where user_id = jwt_user_id
        stmt = db.select(Staff).filter_by(staff_id=staff_id)
        staff = db.session.scalar(stmt)

        # For edge case where old JWT token is used for a deleted account
        if staff is None:
            return {
                "error": "The logged in staff member has been deleted. Please login again."
            }, 403

        # Run the decorated function if staff member is admin
        if staff.is_admin:
            return fn(*args, **kwargs)

        # Else, return error that staff member is not an admin
        else:
            return {
                "error": "Staff member does not have admin privilleges"
            }, 403

    return wrapper

    #Update staff here?
    #Delete staff here?
@auth_bp.route("/staff", methods=["PUT", "PATCH"])
@jwt_required()
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
            return {"error": "Staff member is not authorised to perform this deletion."}, 403
        # update the fields
        # add staff_email or instead of organisation_name?
        staff.organisation_name = body_data.get("organisation_name") or staff.organisation_name
        #staff.staff_email=body_data.get("staff_email") or staff.staff_email
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
@auth_as_admin_decorator
def delete_staff(staff_id):
    # find the staff member with the id from DB
    stmt = db.select(Staff).filter_by(id=staff_id)
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