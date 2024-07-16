from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp
#from marshmallow.validate import Length, And, Regexp?

class Staff(db.Model):
    # name of the table
    __tablename__ = "staff"

    # attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    organisation_name = db.Column(db.String, nullable=False)
    staff_email = db.Column(db.String, nullable=False, unique=True)
    staff_password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    #is_admin = db.Column(db.Boolean, default=False)
    enteredby = db.relationship("EnteredBy", back_populates="staff")
    #forward or back?


class StaffSchema(ma.Schema):
 #   cards = fields.List(fields.Nested('CardSchema', exclude=["staff"]))
  #  comments = fields.List(fields.Nested('CommentSchema', exclude=["staff"]))
    
  #  organisation_name =
    staff_email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format"))

    staff_password = fields.String(required=True, validate=Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", error="Minimum eight characters, at least one letter and one number"))

    #user_library = fields.List(fields.Nested("User_Library_Schema", only=["user_library_id"]))

    class Meta:
        fields = ("id", "organisation_name", "staff_email", "staff_password", "is_admin")


# to handle a single staff object
staff_schema = StaffSchema(exclude=["password"])

# to handle a list of staff objects
staffs_schema = StaffSchema(many=True, exclude=["password"])