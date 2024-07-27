from datetime import date

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.item import Item, item_schema, items_schema
#from utils import authorise_as_admin          
            
item_bp = Blueprint("item", __name__, url_prefix="/item")
                #or items?
          

@item_bp.route("/", methods=["GET"]) 
def get_all_items():
    stmt = db.select(Item).order_by(Item.item_name)
    items = db.session.scalars(stmt)
    return items_schema.dump(items)
            
@item_bp.route("/<int:item_id>")
def get_one_item(item_id):
    stmt = db.select(Item).filter_by(id=item_id)
   
    item = db.session.scalar(stmt)
    if item:
        return item_schema.dump(item)
    else:
        return {"error": f"Item with id {item_id} not found"}, 404

@item_bp.route("/", methods=["POST"])
@jwt_required()
def new_item():
    # get the data from the body of the request
    body_data = item_schema.load(request.get_json())
    # create a new Item model instance
    item = Item(
        item_name=body_data.get("item_name"),
        description=body_data.get("description"),
        quantity=body_data.get("quantity"),
        date_found=date.today(),
        time_found=body_data.get("time_found"),
        location_found=body_data.get("location_found"),
        now_claimed=body_data.get("now_claimed"),
        staffprofile_id=get_jwt_identity(),         
        staff_id=get_jwt_identity(),

    )
    # add and commit to DB
    db.session.add(item)
    db.session.commit()
    # respond
    return item_schema.dump(item), 201

@item_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
#@authorise_as_admin  # is_admin = True
def delete_item(item_id):

    stmt = db.select(Item).filter_by(id=item_id)
    item = db.session.scalar(stmt)

    # If item record exists, delete the item from the session and commit
    if item:
#       is_admin = authorise_as_admin()
#        if not is_admin and str(item.staff_id) != get_jwt_identity():
        if str(item.staff_id) != get_jwt_identity():
            return {"error": "Staff member is not authorised to perform this deletion."}, 403
        db.session.delete(item)
        db.session.commit()
        return {
            "message": f"Item '{item.item_name}' has been deleted successfully"
        }

    # Else return an error message
    else:
        return {"error": f"Item with id {item_id} not found"}, 404
    
@item_bp.route("/<int:item_id>", methods=["PUT", "PATCH"])
@jwt_required()
#@authorise_as_admin  # is_admin = True
def update_item(item_id):

    # Get the item data to be updated from the body of the request
    body_data = item_schema.load(request.get_json(), partial=True)

    stmt = db.select(Item).filter_by(id=item_id)
    item = db.session.scalar(stmt)

    # If item record exists, update the specified fields
    if item:
        if str(item.staff_id) != get_jwt_identity():
            return {"error": "Only authorised staff members can edit item details"}, 403
        
        item.item_name = body_data.get("item_name") or item.item_name
        item.description = body_data.get("description") or item.description
        item.quantity = body_data.get("quantity") or item.quantity
        item.time_found = body_data.get("time_found") or item.time_found
        item.location_found = body_data.get("location_found") or item.location_found
        item.now_claimed = body_data.get("now_claimed") or item.now_claimed

        # Commit the changes
        db.session.commit()

        # Return the updated item back
        return item_schema.dump(item)

    # Else return an error message
    else:
        return {"error": f"Item with id {item_id} not found"}, 404

