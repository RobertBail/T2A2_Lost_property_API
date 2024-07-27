from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp
from marshmallow.exceptions import ValidationError
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
 
class StaffProfile(db.Model):
    __tablename__ = "staffprofiles"

    staffprofile_id = db.Column(db.Integer, primary_key=True)
    staff_name = db.Column(db.String, nullable=False)
    role = db.Column(db.String)

    staff_id = db.Column(db.Integer, db.ForeignKey("staffs.staff_id"), nullable=False)
    staff = db.relationship("Staff", back_populates="staffprofile", cascade="all, delete")
    item = db.relationship("Item", back_populates="staffprofile")

class StaffProfileSchema(ma.Schema):
    staff_id = fields.Int()
    #staffprofile_id = fields.Integer()
    #or staff
    
    staff_name = fields.String(required=True, validate=And(
        Length(min=2, error="Staff Name must be at least 2 characters long"),
        Regexp("^[a-zA-Z0-9\s\-_.'()! ]+$", error="Staff Name cannot contain special characters such as @, &, #, $, %, *, /, question marks, colons, semicolons, and brackets")
    ))
    # StaffName can have hyphen ‐  ?
    role = fields.String()

    class Meta:
        fields = ("staffprofile_id", "staff_name", "role", "staff_id",)
 #        fields = ("staffprofile_id", "StaffName", "role", "staff_id", "staff", "item")   
        #ordered = True
staffprofile_schema = StaffProfileSchema()
staffprofiles_schema = StaffProfileSchema(many=True)