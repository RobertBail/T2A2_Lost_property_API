from datetime import date
#or from datetime import datetime
#from pytz import timezone

#local_timezone = timezone('Australia/Sydney')  # Replace with your timezone

# Get current time in the specified timezone
#current_time = datetime.now(local_timezone)
# For working with timezones (optional but recommended)
#I was seeing if there is a way to record or set the user/staff member's current time of entry, according to their timezone

from flask import Blueprint

from init import db, bcrypt
from models.staff import Staff
from models.enteredby import EnteredBy
from models.item import Item
from models.claimedby import ClaimedBy

#enteredby = some_value

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")

def seed_tables():
    # create a list of Staff instances
    staff = [
        Staff(
            #add organisation_name?
            organisation_name="Nick's Gym",
            staff_email="admin@email.com",
            staff_password=bcrypt.generate_password_hash("test1pw%").decode("utf-8"),
            is_admin=True,
            #enteredby=enteredby[0]
        ),
        Staff(
            organisation_name="Nick's Gym",
            staff_email="staff1@nicks.com",
            staff_password=bcrypt.generate_password_hash("staff1pw!").decode("utf-8"),
            #enteredby=enteredby[1]
        ),
        Staff(
            organisation_name="Nick's Gym",
            staff_email="staff2@nicks.com",
            staff_password=bcrypt.generate_password_hash("staff2pw#").decode("utf-8"),
            #enteredby=enteredby[2],
        ),
        Staff(
            organisation_name="Nick's Gym",
            staff_email="Julia3staff@nicks.com",
            staff_password=bcrypt.generate_password_hash("Julia3staffPW$").decode("utf-8"),
            #enteredby=enteredby[3],
        )
    ]

    db.session.add_all(staff)

# for the purpose of a staff account/enteredby details table
    enteredby = [
        EnteredBy(
            StaffName="Keith Smith",
            role="Admin Manager",
            staff=staff[0]
            #add anything else?  
            #item=items[0],
        ),
        EnteredBy(
            StaffName="Gerald Simmons",
            role="Teacher",
            staff=staff[1]
        ),
        EnteredBy(
            StaffName="Julia Burns",
            role="Swimming Instructor",
            staff=staff[2]
        )
    ]

    db.session.add_all(enteredby)

    item = [
        Item(
            item_name="Adidas T-Shirt",
            description="black and white large",
            quantity="1",
            date_found=date.today(),
            time_found ="4:00PM",
            #staff/user enters time manually
            location_found="locker room under bench",
            now_claimed="Yes",
            enteredby=enteredby[0],
            staff=staff[0]
            # id? or relationship?
        ),
         Item(
            item_name="Kathmandu backpack",
            description="blue Cotinga 30L",
            quantity="1",
            date_found=date.today(),
            time_found ="2:00PM",
            location_found="next to bins",
            now_claimed="Yes",
            enteredby=enteredby[1],
            staff=staff[1]
            # id?
        ),
        Item(
            item_name="Earrings",
            description="gold hoops",
            quantity="2",
            date_found=date.today(),
            time_found ="10:00AM",
            location_found="locker room shower",
            now_claimed="No",
            enteredby=enteredby[2],
            staff=staff[2]
            # id?
        ),
    ]

    db.session.add_all(item)
 
    claimedby = [
        ClaimedBy(
    #information to know who collected the item and when, eg. in case of mix-ups, theft even perhaps
            name="Tim Johnson",
            phone="0200010110",
            email="tjohnson100@aol.com",
            address="222 Bank St Sydney",
            date_claimed=date.today(),
            item=item[0],
        #reference items id?
        #reference staff id?
        ),
        ClaimedBy(
            name="Samantha Gold",
            phone="0600050110",
            email="sgold33@gmail.com",
            address="444 Smith St Mascot",
            date_claimed=date.today(),
            item=item[1],
        #reference items id?
        #reference staff id?
        ),
        #ClaimedBy(
        #    name="Larry Field",
        #    phone="0770090110",
        #    email="larryfield777@yahoo.com",
        #    address="999 Jones Tce Smithfield",
        #    date_claimed=date.today(),
        #    item=items[2],
        #reference items id?
        #reference staff id?
       # ),
    ]

    db.session.add_all(claimedby)

    db.session.commit()

    print("Tables seeded")