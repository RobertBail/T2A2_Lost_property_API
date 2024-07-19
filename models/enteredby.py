from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp
from marshmallow.exceptions import ValidationError
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
 
class EnteredBy(db.Model):
    __tablename__ = "enteredbys"

    enteredby_id = db.Column(db.Integer, primary_key=True)
    StaffName =  db.Column(db.String, nullable=False)
    role = db.Column(db.String)

    staff_id = db.Column(db.Integer, db.ForeignKey("staffs.staff_id"), nullable=False)
    staff = db.relationship("Staff", back_populates="enteredby")

class EnteredBySchema(ma.Schema):

    #or staff
    staff = fields.Nested('StaffSchema', only=["staff_id", "organisation_name", "staff_email"])

    StaffName = fields.String(required=True, validate=And(
        Length(min=2, error="Staff Name must be at least 2 characters long"),
        Regexp("^[a-zA-Z0-9\s\-_.'()! ]+$", error="Staff Name cannot contain special characters such as @, &, #, $, %, *, /, question marks, colons, semicolons, and brackets")
    ))
    # StaffName can have hyphen ‐  ?
    #this for "role" also?

    class Meta:
        fields = ("enteredby_id", "StaffName", "role")
    

enteredby_schema = EnteredBySchema()
enteredbys_schema = EnteredBySchema(many=True)