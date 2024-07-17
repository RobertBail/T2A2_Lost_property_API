from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, Range

#all claimedby can be nullable
class ClaimedBy(db.Model):
    __tablename__ = "claimedbys"
    
    claimedby_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.Integer)
    email = db.Column(db.String, unique=True)
    address = db.Column(db.String)
    date_claimed = db.Column(db.Date)

    #item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    #item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    items = db.relationship("Item", back_populates="claimedbys")
   
class ClaimedBySchema(ma.Schema):
   
   items = fields.Nested('ItemSchema', only=["item_id", "item_name"])
   #item = fields.Nested('ItemSchema', only=["item_id", "item_name"])

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
#need required=True here?
   email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format"))

   phone = fields.Integer(
        required=True,
        validate=Range(
            min=6,
            max=10,
            error="Phone number must be minimum 6 and maximum 10 numbers",
        ),
    )
   
   #address also?

   class Meta:
        fields = (
            "claimedby_id",
            "name",
            "phone",
            "email",
            "address",
            "date_claimed",
        )

claimedby_schema = ClaimedBySchema()
claimedbys_schema = ClaimedBySchema(many=True)