#from datetime import date
from datetime import datetime

from init import db, ma
from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

from marshmallow.validate import Length, And, Regexp, OneOf, Range

VALID_STATUSES = ( "Yes", "No" )

class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String)
    description = db.Column(db.String)
    quantity = db.Column(db.Integer) 
    date_found = db.Column(db.Date)
    time_found = db.Column(db.String)
    #I kept time_found as "String" eg. to type in 4:00PM
    location_found = db.Column(db.String)
    now_claimed = db.Column(db.String)

    staffprofile_id = db.Column(db.Integer, db.ForeignKey("staffprofiles.staffprofile_id"), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("staffs.staff_id"), nullable=False)
    #claimedby_id = db.Column(db.Integer, db.ForeignKey("claimedbys.claimedby_id"))

    staffprofile = db.relationship("StaffProfile", back_populates="item", cascade="all, delete")
    #staffprofile = db.relationship("StaffProfile", back_populates="item")
    staff = db.relationship("Staff", back_populates="item")
    #staff = db.relationship("Staff", back_populates="item")
    claimedby = db.relationship("ClaimedBy", back_populates="item")

class ItemSchema(ma.Schema):
    id = fields.Integer()
    staffprofile_id = fields.Integer()
    staff_id = fields.Integer()
  
    staffprofile = fields.Nested('StaffProfileSchema', only=["StaffName"])
    #staffprofiles = fields.Nested('StaffProfileSchema')  for all fields in staffprofiles including "staffprofile_id"?
    #staffprofile = fields.Nested('StaffProfileSchema', only=["StaffName"])
    staff = fields.Nested('StaffSchema', only=["id", "organisation_name", "staff_email"])
    #staff = fields.Nested('StaffSchema', only=["staff_id", "organisation_name", "staff_email"])
    #claimedby = fields.Nested('ClaimedBySchema', only=["claimedby_id", "name"])

    #item_id = fields.Integer()
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
    time_found = fields.String()
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
            "id",
            "item_name",
            "description",
            "quantity",
            "date_found",
            "time_found",
            "location_found",
            "now_claimed",
            "staffprofile_id",
            "staff_id",
            
        )
        ordered = True

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

