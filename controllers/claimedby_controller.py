from datetime import date

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.claimedby import ClaimedBy, claimedby_schema, claimedbys_schema
#from controllers.item_controller import item_bp
#from utils import authorise_as_admin

claimedby_bp = Blueprint("claimedby", __name__, url_prefix="/claimedby")
#claimedby_bp.register_blueprint(item_bp) 

#desc() meaning sort the result in a descending order.
@claimedby_bp.route('/', methods=["GET"])
def get_all_claimedbys():
    stmt = db.select(ClaimedBy).order_by(ClaimedBy.name)
    claimedby = db.session.scalars(stmt)
    return claimedbys_schema.dump(claimedby)  

@claimedby_bp.route('/<int:claimedby_id>')
def get_one_claimedby(claimedby_id):

    stmt = db.select(ClaimedBy).filter_by(id=claimedby_id)
    claimedby = db.session.scalar(stmt)
    if claimedby:
        return claimedby_schema.dump(claimedby)
    else:
        return {"error": f"Claimedby with id {claimedby_id } not found"}, 404

@claimedby_bp.route('/', methods=["POST"])
@jwt_required()
def new_claimedby():
    body_data = claimedby_schema.load(request.get_json())
    # Create a new claimedby model instance
    claimedby = ClaimedBy(
        name = body_data.get('name'),
        phone = body_data.get('phone'),
        email = body_data.get('email'),
        address = body_data.get('address'),
        date_claimed = date.today(),
        item_id = get_jwt_identity(),
        staff_id = get_jwt_identity()
    )
    # Add that to the session and commit
    db.session.add(claimedby)
    db.session.commit()
    # return the newly created claimedby
    return claimedby_schema.dump(claimedby), 201

@claimedby_bp.route("/<int:claimedby_id>", methods=["DELETE"])
#@jwt_required()
def delete_claimedby(claimedby_id):
    
    stmt = db.select(ClaimedBy).filter_by(id=claimedby_id)
    claimedby = db.session.scalar(stmt)
    # if claimedby exists
    if claimedby:
        # delete the claimedby
        db.session.delete(claimedby)
        db.session.commit()
        # return some message
        return {"message": f"Claimedby '{claimedby.name}' deleted successfully"}
    # else
    else:
        # return an error saying claimedby does not exist
        return {"error": f"Claimedby with id {claimedby_id} not found"}, 404

@claimedby_bp.route("/<int:claimedby_id>", methods=["PUT", "PATCH"])
#@jwt_required()
def update_claimedby(claimedby_id):
    # get the data from the body of the request
    body_data = claimedby_schema.load(request.get_json(), partial=True)
    # get the claimedby from the database
    stmt = db.select(ClaimedBy).filter_by(id=claimedby_id)
    claimedby = db.session.scalar(stmt)
    # if claimedby exists
    if claimedby:
        # if the item does not match the claimedby
    #    if str(card.item_id ) != get_jwt_identity():
    #        return {"error": "item does not match the claimedby"}, 403
        # update the fields as required
        claimedby.name = body_data.get("name") or claimedby.name
        claimedby.phone = body_data.get("phone") or claimedby.phone
        claimedby.email = body_data.get("email") or claimedby.email
        claimedby.address = body_data.get("address") or claimedby.address
        # commit to the DB
        db.session.commit()
        # return a response
        return claimedby_schema.dump(claimedby)
    # else
    else:
        # return an error
        return {"error": f"Claimedby with id {claimedby_id} not found"}, 404


