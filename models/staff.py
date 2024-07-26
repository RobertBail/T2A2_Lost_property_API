from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp
#from marshmallow.validate import Length, And, Regexp?
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Staff(db.Model):
    # Name of the table. I know staffs isn't correct grammar, but to simplify and not confuse terminology/references too much
    __tablename__ = "staffs"

    # attributes of the table
    staff_id = db.Column(db.Integer, primary_key=True)
    organisation_name = db.Column(db.String)
    staff_email = db.Column(db.String, nullable=False, unique=True)
    staff_password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    #is_admin = db.Column(db.Boolean, default=False)
    item = db.relationship("Item", back_populates="staff")
    #plural or single? item = db.relationship("Item", back_populates="staff")
    staffprofile = db.relationship("StaffProfile", back_populates="staff")
    claimedby = db.relationship("ClaimedBy", back_populates="staff")
    #forward or back?


class StaffSchema(ma.Schema):
    staff_id = fields.Integer()
    #item = fields.Nested("ItemSchema", only=["item_id", "item_name"])
    #enteredby = fields.Nested("EnteredBySchema", exclude=["enteredby_id"])
   
    organisation_name = fields.String(validate=And(
            Length(min=2,
                   error="Organisation name must have a length of at least 2 characters"),
            Regexp("^[a-zA-Z0-9\s\-_.'()! ]+$",
                   error="Organisation name cannot contain special characters such as @, &, #, $, %, *, /, question marks, colons, semicolons, and brackets"),
        ),
    )
    staff_email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format"))

    staff_password = fields.String(
            required=True,
            validate=(
            Length(
                min=6, error="Password must be at least 6 characters long."
            ),
            #Regexp(
            #    "[a-zA-Z0-9_.-]+$^",
            #    error="Password must be unspaced and contain valid characters.",
            #),
        ),
    #       load_only=True,
    )

    class Meta:
        fields = ("staff_id", 
                  "organisation_name", 
                  "staff_email", 
                  "staff_password", 
                  "is_admin", 

                  )


# to handle a single staff object
staff_schema = StaffSchema()

# to handle a list of staff objects
staffs_schema = StaffSchema(many=True, exclude=["staff_password"])