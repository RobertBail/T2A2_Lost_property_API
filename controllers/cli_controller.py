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
from models.staffprofile import StaffProfile
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
    staffs = [
        Staff(
            staff_id=1,
            organisation_name="Nick's Gym",
            staff_email="admin@email.com",
            staff_password=bcrypt.generate_password_hash("test1pw%").decode("utf-8"),
            is_admin=True,
        ),
        Staff(
            staff_id=2,
            organisation_name="Nick's Gym",
            staff_email="Geraldsimmons1@nicks.com",
            staff_password=bcrypt.generate_password_hash("staff1pw!").decode("utf-8"),
        ),
        Staff(
            staff_id=3,
            organisation_name="Nick's Gym",
            staff_email="Julia1staff2@nicks.com",
            staff_password=bcrypt.generate_password_hash("staff2pw#").decode("utf-8"),
        ),
        Staff(
            staff_id=4,
            organisation_name="Nick's Gym",
            staff_email="AnthonyS3staff@nicks.com",
            staff_password=bcrypt.generate_password_hash("Julia3staffPW$").decode("utf-8"),
        )
    ]

    db.session.add_all(staffs)

# for the purpose of a staff details table
    staffprofiles = [
        StaffProfile(
            staffprofile_id=1,
            StaffName="Admin",
            role="Admin",
            staff_id=1
            #add anything else?  
            #item=items[0],
        ),
        StaffProfile(
            staffprofile_id=2,
            StaffName="Gerald Simmons",
            role="Teacher",
            staff_id=2
        ),
        StaffProfile(
            staffprofile_id=3,
            StaffName="Julia Burns",
            role="Swimming Instructor",
            staff_id=3
        ),
        StaffProfile(
            staffprofile_id=4,
            StaffName="Anthony Stevens",
            role="Personal Trainer",
            staff_id=4
        )
    ]

    db.session.add_all(staffprofiles)

    items = [
        Item(
            item_name="Adidas T-Shirt",
            description="black and white large",
            quantity="1",
            date_found=date.today(),
            time_found ="4:00PM",
            #staff/user enters time manually
            location_found="locker room under bench",
            now_claimed="Yes",
            staffprofile_id=1,
            staff_id=1
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
            staffprofile_id=2,
            staff_id=2
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
            staffprofile_id=3,
            staff_id=3
            # id?
        ),
    ]

    db.session.add_all(items)
 
    claimedbys = [
        ClaimedBy(
    #information to know who collected the item and when, eg. in case of mix-ups, theft even perhaps
            name="Tim Johnson",
            phone="0200010110",
            email="tjohnson100@aol.com",
            address="222 Bank St Sydney",
            date_claimed=date.today(),
            staff_id=1,
            item_id=1,
        #reference items id?
        #reference staff id?
        ),
        ClaimedBy(
            name="Samantha Gold",
            phone="0600050110",
            email="sgold33@gmail.com",
            address="444 Smith St Mascot",
            date_claimed=date.today(),
            staff_id=2,
            item_id=2,
            
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

    db.session.add_all(claimedbys)

    db.session.commit()

    print("Tables seeded")