from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, Range

#all claimedby can be nullable
class ClaimedBy(db.Model):
    __tablename__ = "claimedbys"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.Integer)
    email = db.Column(db.String, unique=True)
    address = db.Column(db.String)
    date_claimed = db.Column(db.Date)

    #item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    staff_id = db.Column(db.Integer, db.ForeignKey("staffs.staff_id"))
    #items = db.relationship("Item", back_populates="claimedby")
    item = db.relationship("Item", back_populates="claimedby")
    staff = db.relationship("Staff", back_populates="claimedby")
   
class ClaimedBySchema(ma.Schema):
   #id = fields.Integer()
   staff_id = fields.Integer()
   item_id = fields.Integer()

   item = fields.Nested('ItemSchema', only=["item_name"])
   #item = fields.Nested('ItemSchema', only=["item_id", "item_name"])
   staff = fields.Nested('StaffSchema', only=["staff_email"])

   name = fields.String(
        required=True,
        validate=And(
            Length(
                min=2,
                error="Name must have a length of at least 2 characters",
            ),
            Regexp(
                "^[a-zA-Z0-9\s\-_&.'()! ]+$",
                error="Name cannot contain special characters such as @, #, $, %, *, /, question marks, colons, semicolons, and brackets",
            ),
        ),
    )

#this stopped working properly for some reason, 27-7-2024 11pm approx. Kept getting "TypeError: object of type 'int' has no len()" Tried for a while to sort this out eg. if indentation issue or other formatting
#if I try to remove "" for eg. phone="0200010110" in cli_controller, terminal gives me "SyntaxError: leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers"
#Phone numbers/Integers seem to be only accepted without zeros in front in Insomnia
#   phone = fields.Integer(       
#        required=True,
#        validate=(
#            Length(
#                min=6, error="Phone number must have a length of at least 6 numbers",
#            ),
#        ),
#    )
  
#this version stopped working for some reason, eg. if putting 9 or 10 numbers in Insomnia
#        validate=Range(
#                min=6,
#                max=10,
#            ),
#        ),
#    )       
#need required=True here?
   email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format"))

   #address also?

   class Meta:
        fields = (
            "id",
            "name",
            "phone",
            "email",
            "address",
            "date_claimed",
            "item_id",
            "staff_id"
        )
        ordered = True
claimedby_schema = ClaimedBySchema()
claimedbys_schema = ClaimedBySchema(many=True)