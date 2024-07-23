from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp
from marshmallow.exceptions import ValidationError
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
 
class StaffProfile(db.Model):
    __tablename__ = "staffprofiles"

    staffprofile_id = db.Column(db.Integer, primary_key=True)
    StaffName = db.Column(db.String, nullable=False)
    role = db.Column(db.String)

    staff_id = db.Column(db.Integer, db.ForeignKey("staffs.staff_id"), nullable=False)
    staff = db.relationship("Staff", back_populates="staffprofile")
    item = db.relationship("Item", back_populates="staffprofile")

class StaffProfileSchema(ma.Schema):
    #id = fields.Int()
    id = fields.Integer()
    #or staff
    #staff = fields.Nested('StaffSchema', only=["staff_id", "organisation_name", "staff_email"])
    #staff = fields.Nested('StaffSchema', only=["organisation_name", "staff_email"])
    StaffName = fields.String(required=True, validate=And(
        Length(min=2, error="Staff Name must be at least 2 characters long"),
        Regexp("^[a-zA-Z0-9\s\-_.'()! ]+$", error="Staff Name cannot contain special characters such as @, &, #, $, %, *, /, question marks, colons, semicolons, and brackets")
    ))
    # StaffName can have hyphen ‐  ?
    #this for "role" also?

    class Meta:
        fields = ("staffprofile_id", "StaffName", "role", "staff_id",)
 #        fields = ("staffprofile_id", "StaffName", "role", "staff_id", "staff", "item")   
        ordered = True
staffprofile_schema = StaffProfileSchema()
staffprofiles_schema = StaffProfileSchema(many=True)