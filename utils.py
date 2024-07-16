import functools

from flask_jwt_extended import get_jwt_identity

from init import db
from models.staff import Staff

def authorise_as_admin():
    # get the user's id from get_jwt_identity
    user_id = get_jwt_identity()
    # fetch the user from the db
    stmt = db.select(Staff).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # check whether the user is an admin or not
    return user.is_admin
# change user to staff?
def auth_as_admin_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # get the user's id from get_jwt_identity
        user_id = get_jwt_identity()
        # fetch the entire user using the id
        stmt = db.select(Staff).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        # if user is an admin
# change user to staff?
        if user.is_admin:
            # allow the decorated function to execute
            return fn(*args, **kwargs)
        # else (user is not an admin)
        else:
            # return error
            return {"error": "Only admin can perform this action"}, 403

    return wrapper