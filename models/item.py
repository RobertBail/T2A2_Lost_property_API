#from datetime import date
from datetime import datetime

from init import db, ma
from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

from marshmallow.validate import Length, And, Regexp, OneOf, Range

VALID_STATUSES = ( "Yes", "No" )

class Item(db.Model):
    __tablename__ = "items"

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer) 
    date_found = db.Column(db.Date)
    time_found = db.Column(db.String)
    #I kept time_found as "String" eg. to type in 4:00PM
    location_found = db.Column(db.String)
    now_claimed = db.Column(db.String)

    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)
    enteredby_id = db.Column(db.Integer, db.ForeignKey("enteredby.id"), nullable=False)

    enteredbys = db.relationship("EnteredBy", back_populates="items", cascade="all, delete")
    #enteredby = db.relationship("EnteredBy", back_populates="item")
    staffs = db.relationship("Staff", back_populates="items")
    #staff = db.relationship("Staff", back_populates="item")
    #for claimedby  also?

class ItemSchema(ma.Schema):
  
    enteredbys = fields.Nested('EnteredBySchema', only=["StaffName"])
    #enteredbys = fields.Nested('EnteredBySchema')  for all fields in enteredbys including "enteredby_id"?
    #enteredby = fields.Nested('EnteredBySchema', only=["StaffName"])
    staffs = fields.Nested('StaffSchema', only=["staff_id", "organisation_name", "staff_email"])
    #staff = fields.Nested('StaffSchema', only=["staff_id", "organisation_name", "staff_email"])
    #for claimedby  also?

    item_id = fields.Integer()
    item_name = fields.String(
        required=True,
        validate=And(
            Length(
                min=2,
                error="Item name must have a length of at least 2 characters",
            ),
            Regexp(
                "^[a-zA-Z0-9\s\-_&.'()! ]+$",
                error="Item name cannot contain special characters such as @, #, $, %, *, /, question marks, colons, semicolons, and brackets",
            ),
        ),
    )
    #not allowed commas in input strings?
    description = fields.String(
        required=True,
        validate=And(
            Length(
                min=2,
                error="Description must have a length of at least 2 characters",
            ),
            Regexp(
                "^[a-zA-Z0-9\s\-_&.'()! ]+$",
                error="Description cannot contain special characters such as @, #, $, %, *, /, question marks, colons, semicolons, and brackets",
            ),
        ),
    )
   # date_found = fields.Date(
   #     format="%Y-%m-%d",
   #     error_messages={"error": "Invalid date format. Use YYYY-MM-DD."},
   # )

    #@validates("date_found")
    #def validate_release_date(self, value):
    #    if value > datetime.now().date():
     #       raise ValidationError("Release date cannot be in the future.")

    quantity = fields.Integer(
        validate=Range(
            min=0,
            max=99999999,
            error="Quantity must be a whole number",
        ),
    )
    
    now_claimed = fields.String(validate=OneOf(VALID_STATUSES, error="Invalid option or entry"))
 #  now_claimed = fields.String(validate=OneOf(VALID_STATUSES))

# @validates("now_claimed") needed?
#    @validates("now_claimed")
#    def validate_status(self, value):
        # if trying to set the value of status as "Ongoing"
#        if value == VALID_STATUSES[1]:
            # check whether an existing claimedby exists or not
 #           stmt = db.select(db.func.count()).select_from(Item).filter_by(status=VALID_STATUSES[1])
 #           count = db.session.scalar(stmt)
            # if it exists
 #           if count > 0:
                # throw error
 #               raise ValidationError("Invalid option or entry")

    class Meta:
        fields = (
            "item_id",
            "item_name",
            "description",
            "quantity",
            "date_found",
            "time_found",
            "location_found",
            "now_claimed",
        )


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

