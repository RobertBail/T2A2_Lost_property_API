from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp
#from marshmallow.validate import Length, And, Regexp?

class Staff(db.Model):
    # Name of the table. I know staffs isn't correct grammar, but to simplify and not confuse terminology/references too much
    __tablename__ = "staffs"

    # attributes of the table
    staff_id = db.Column(db.Integer, primary_key=True)
    organisation_name = db.Column(db.String, nullable=False)
    staff_email = db.Column(db.String, nullable=False, unique=True)
    staff_password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    #is_admin = db.Column(db.Boolean, default=False)
    items = db.relationship("Item", back_populates="staff")
    #plural or single? item = db.relationship("Item", back_populates="staff")
    #enteredby = db.relationship("EnteredBy", back_populates="staff")
    #forward or back?


class StaffSchema(ma.Schema):
    items = fields.Nested('ItemSchema', only=["item_id", "item_name"])
   
    organisation_name = fields.String(required=True, validate=And(
            Length(min=2,
                   error="Organisation name must have a length of at least 2 characters"),
            Regexp("^[a-zA-Z0-9\s\-_.'()! ]+$",
                   error="Organisation name cannot contain special characters such as @, &, #, $, %, *, /, question marks, colons, semicolons, and brackets"),
        ),
    )
    staff_email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format"))

    staff_password  = fields.String(
            required=True,
            validate=And(
            Length(
                min=6, error="Password must be at least 6 characters long."
            ),
            Regexp(
                "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$",
                error="Password must include at least one letter, one number, and one special character.",
            ),
        ),
    #       load_only=True,
    )

    class Meta:
        fields = ("staff_id", "organisation_name", "staff_email", "staff_password", "is_admin")


# to handle a single staff object
staff_schema = StaffSchema(exclude=["staff_password"])

# to handle a list of staff objects
staffs_schema = StaffSchema(many=True, exclude=["staff_password"])