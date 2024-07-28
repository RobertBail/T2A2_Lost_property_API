# T2A2_Lost_property_API

[Github Repository](https://github.com/RobertBail/T2A2_Lost_property_API)

[Trello Board](https://trello.com/b/ZxhUNEZr/lost-property-api)

## How to Set Up

To run this app from a local machine:
1. Clone this API to your local machine from the GitHub repo above
2. Open the 'src' folder in your terminal of choice
3. Create a postgresql database:
```py
CREATE DATABASE lost_propertydb;
```
4. Create a new postgresql user, such as your name or org's name, and give permissions from within Postgres interface, eg.:
```py
CREATE ROLE lostproperty_dev && GRANT ALL ON lost_propertydb TO lostproperty_dev;
```
5. Edit the ".env" file so "SQL_DATABASE_URI" matches the user and database details, eg.:
```py
DATABASE_URI="postgresql+psycopg2://lostproperty_dev:123456@localhost:5432/lost_propertydb"
JWT_SECRET_KEY="secret"
```
6. Start & activate virtual environment:
```py
python3 -m venv venv && source .venv/bin/activate
```
A variation of this can be:
```py
python3 -m venv src/.venv && source .venv/bin/activate
```
7. Install requirements:
```py
pip3 install -r requirements.txt
```
8. Create and seed tables:
```py
python3 -m flask db drop && python3 -m flask db create && python3 -m flask db seed
```
9. Run flask app:
```py
python3 -m flask run
```

This can also work:
```py
flask run
```
## Purpose and Aim
The Lost Property API will assist organisations to keep track and manage lost property. Such organisations could include schools, gyms, sports stadiums, hotels, airports, train stations, bus stations, and other larger workplaces.

Lost property, otherwise known as lost and found, can be a significant problem for organisations to face and manage. For instance, it is a common experience for customers to lose valuables in places such as hotels, airports and music venues, and these places have no system for logging and tracking these items (Coleman 2023). Hence, lost and found can turn into a "customer service problem faced by businesses of all sizes" (Coleman 2023). For instance, customers may not know what to do when they lose valuables, and the person who lost the item and the person who found it may never find each other, so implementing a system to track and manage lost property can enhance the customer experience (Coleman 2023). The Lost Property API aims to help solve these issues for organisations, whereby staff of a particular organisation can keep track of customers' or other staff members' lost property.

When staff log in and register to the Lost Property API, they can specify details such as the organisation name, along with their email address and password. After staff log in, they can enter their name and role in the organisation, to inform other staff of this. This would be particularly helpful in busy organisations with a larger workforce, such as those listed above, where some staff may not know other staff, such as if they're new staff.

Staff of these organisations can register and log into this database, and provide details of items that have been left behind, such as the item name, description, quantity, time found, location found, and if it has been now claimed, either "Yes" or "No" for this. The date these item details are entered will be recorded automatically. 

Staff can also enter details of who has claimed the item, when that occurs. These are referred to as "Claimed By" details, to inform staff of who has collected the item and when. The Claimed By details could be helpful in case of mix-ups or even theft by customers or staff who collect items. The Claimed By details include the claimer/owner's name, phone number, email address, physical address, and the date claimed will be recorded automatically.

Reference:
Coleman, A 2023, "How Solving The Age-Old Lost And Found Dilemma Enhances Customer Experience" Forbes, accessed 28 July 2024, https://www.forbes.com/sites/alisoncoleman/2023/04/25/how-solving-the-age-old-lost-and-found-dilemma-enhances-customer-experience/

## How tasks are allocated and tracked

I used Trello to plan and track the completion of this project, including for time management. I developed this app over approximately two weeks, or 16 days. I began this project on Friday 12 July 2024, by creating a draft ERD. I primarily made the first week, Monday 15 July to Friday 19 July, the week for writing the files. And I made the second week until 27 July, mainly for testing and fine-tuning the app. There also happened to be some troubleshooting throughout the second week, which I made comments on in Trello. 

Admittedly, I'm not entirely familiar with using Trello still, but I decided to comment/sort-of blog as I was progressing through the project, eg. some challenges/problems to solve, ie. the troubleshooting throughout the second week. When doing these projects I often use a notepad/txt file (eg. API_project.txt) to write out certain things, bits of code to use/try out, reminders, etc. I decided to include this API_project.txt file in the docs folder, as an informal example.

### Trello Board Overall
![trello 1](./docs/trello_LP1.png)
### Planning/Draft ERD phase
![trello 2](./docs/trello_LP2.png)
### Beginning of coding, writing files 
![trello 3](./docs/trello_LP3.png)
### Midway completion of Models and Controllers
![trello 4](./docs/trello_LP4.png)
### Initial/primary completion of files 
![trello 5](./docs/trello_LP5.png)
### Beginning of testing and troubleshooting
![trello 6](./docs/trello_LP6.png)
### The completion of testing best as possible
![trello 7](./docs/trello_LP7.png) 
![trello 8](./docs/trello_LP8.png)


## The third-party services, packages and dependencies used in this app
There are overall 22 modules/packages that have been used to develop this app. The primary services and packages include:

### Flask
Flask is a micro web framework written in Python. It provides tools, libraries and technologies to build a web application. Flask also contains extensions which assist with database integration, form validation, upload handling, and open authentication technologies. For instance, Flask can initiate or "flask run" the application, and assist with creating and seeding database tables.

### PostgreSQL
PostgreSQL, also known as Postgres, is a free and open-source relational database management system, which emphasizes extensibility and SQL compliance. PostgreSQL describes itself to be the "world's most advanced open source database" and it is known for its reliability, scalability, and support for advanced data types (PostgreSQL 2024).

### Marshmallow
Marshmallow is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes (Loria 2024). Marshmallow and its schemas can be used to validate input data and deserialize input data to app-level objects, ie. make it useful in apps (Loria 2024). For instance, a marshmallow schema can be used to validate package json files, as relevant in this app (Loria 2024).

### SQLAlchemy
SQLAlchemy is an open-source Python library that provides a SQL toolkit and Object Relational Mapper for database interactions. This library provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, which is adapted into a simple and Pythonic domain language.

### Flask JWT Extended
JWT Extended is an extension for flask that adds support for JSON Web Tokens (JWT). This allows for secure and convenient authentication mechanisms and can be used to protect routes and endpoints. JWT Extended is used in this app to create web access tokens, and check these tokens for identification and authorisation, which will make the app's routes secure.

Statements such as "@jwt_required()" in this app's code will authorise logged-in staff to input and edit certain lost property details, such as for each item and "ClaimedBy", along with their own staff details.

### Bcrypt
Bcrypt is a password hashing library which assists with the safe storage of passwords. The Bcrypt algorithm is designed to be resistant to brute-force search attacks and is a major component for building secure flask applications. In this application, Bcrypt is used to hash staff passwords so they are not stored in plain text, which improves staff/user security, as in this mock-up example in the cli_controller file:

```py
staff_password=bcrypt.generate_password_hash("123456").decode("utf-8"),
```
### Psycopg2
Psycopg is a popular PostgreSQL database adapter for the Python programming language. Its extensions allow access to many of the features offered by PostgreSQL (Varrazzo 2024). Psycopg2 allows the connection to a postgreSQL database to execute SQL queries, fetch data, and perform database operations.

References:
Loria, S 2024 "Examples", Marshmallow, accessed 28 July 2024, https://marshmallow.readthedocs.io/en/stable/examples.html

Loria, S 2024 "marshmallow: simplified object serialization" Marshmallow, accessed 28 July 2024, https://marshmallow.readthedocs.io/en/stable/

PostgreSQL 2024, "PostgreSQL: The World's Most Advanced Open Source Relational Database", PostgreSQL, accessed 28 July 2024, https://www.postgresql.org/

Varrazzo, D 2024 "psycopg" Psycopg, accessed 28 July 2024, https://www.psycopg.org/#:~:text=Psycopg%20is%20the%20most%20popular,the%20features%20offered%20by%20PostgreSQL.

SQLAlchemy 2024 "The Python SQL Toolkit and Object Relational Mapper" SQLAlchemy, accessed 28 July 2024, https://www.sqlalchemy.org/

## The benefits and drawbacks of this app’s underlying database system
Benefits of using Postgres include (IONOS 2022):
- Open source, ie. free to use.
- Highly expandable, eg. unlimited number of rows and unlimited number of indexes.
- Supporting JSON, which has been ideal for this project, such as for testing the API.
- It is possible to process complex data types (e.g. geographical data). It does process the current date for instance, as in the ClaimedBy and Item tables.
- Ability for flexible full text search.

One noticeable disadvantage of Postgres so far (at least indicated in the terminal), is not being able to properly implement the phone number field for the claimedby table, eg. for phone numbers starting with 0, such as 0200010110. If I tried to enter a phone number beginning with 0 in Insomnia, I got an error message such as:
"SyntaxError: leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers".
This system didn't seem to accept numbers, such as phone numbers, beginning with 0. In future, to get around this, I might recommend that staff/users enter these phone numbers without beginning zeros where possible. Also, I was unable to properly implement a minimum and maximum for the phone number field, intended to be between 6 and 10 numbers. I further explained this in comments on my Trello board.

Other disadvantages of Postgres include a comparatively low reading speed and not being available on all hosts by default (IONOS 2022).

Reference:

IONOS 2022, "PostgreSQL: a closer look at the object-relational database management system", IONOS, accessed 28 July 2024, https://www.ionos.com/digitalguide/server/know-how/postgresql/


## The features, purpose and functionalities of the ORM used in this app
An ORM (Object Relational Mapper) is a layer of software that helps map the code Objects to the database. ORMs allow developers to manipulate the database using the programming language's own constructs, eg. for Python in this app, without having to understand the complexities of SQL syntax and database operations.

ORMs can represent database tables as classes and rows as their instances. In this app, data models are used, whereby relational models are represented as classes, which is helpful for relatively easy interaction and making adjustments, such as while testing the API in Insomnia.

```python
# create Item model
class Item(db.Model):
    # set tablename to items
    __tablename__ = "items"
    # use db to define columns and data types
    # set id as primary key
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String)
    description = db.Column(db.String)
    quantity = db.Column(db.Integer) 
    date_found = db.Column(db.Date)
    time_found = db.Column(db.String)
    #I kept time_found as "String" eg. to manually type in 4:00PM
    location_found = db.Column(db.String)
    now_claimed = db.Column(db.String)
```

ORMs also facilitate CRUD operations, ie. creating, reading, updating, and deleting database records, which means developers don't need to write raw SQL queries for these operations. In this app, CRUD operations are handled via requests, eg. via "request", as in the example below. The example below is for POST for adding/creating new item details.

```python
@item_bp.route("/", methods=["POST"])
@jwt_required()
def new_item():
    # get the data from the body of the request
    body_data = item_schema.load(request.get_json())
    # create a new Item model instance
    item = Item(
        item_name=body_data.get("item_name"),
        description=body_data.get("description"),
        quantity=body_data.get("quantity"),
        date_found=date.today(),
        time_found=body_data.get("time_found"),
        location_found=body_data.get("location_found"),
        now_claimed=body_data.get("now_claimed"),
        staffprofile_id=get_jwt_identity(),         
        staff_id=get_jwt_identity(),

    )
    # add and commit to DB
    db.session.add(item)
    db.session.commit()
    # respond
    return item_schema.dump(item), 201
```

ORMs also facilitate query abstraction, ie. querying the database using the chosen programming language. This can make the development process more intuitive/natural and therefore less error-prone than specifically writing SQL queries. This query abstraction is exemplified by:

```python
body_data = item_schema.load(request.get_json())
```

## The entity relationship diagram (ERD) for this app’s database
### An early draft version of the ERD
![Early ERD](./docs/earlydraftERD.png)

Early on, when I created the draft ERD, I had the idea of tables for Staff, Found_By, Item, and Claimed_By. Not long after, I changed Found_By into EnteredBy and then finally StaffProfile, which is more of a proper name for it.

- Staff would be the beginning table, which facilitates register and login of staff members. This also enables the entry of the "organisation_name" into the database, whichever organisation could be using the Lost Property API.
- Staff enables access to the StaffProfile table, with which Staff/users can enter further details about themselves, such as their name and role in their organisation.
- After at least giving their name, entered into StaffProfile, staff/users can enter details of the lost property into the Items table, such as the item name, description, quantity, time found, location found, and if it has been "now claimed", either "Yes" or "No" for this. The date these item details are entered will be recorded automatically.
- When a customer or other staff member claims an item, the details of this claimer can be entered into the ClaimedBy table, such as their name, phone number, email address, physical address, and the date claimed will be recorded automatically. Staff can also then update the "now claimed" field for Item details, ie. changing it to Yes.
- The StaffProfile, Item and ClaimedBy tables all contain a "staff_id" foreign key, to allow Staff access to these tables/entries. Item also contains a staffprofile_id foreign key, which connects from the StaffProfile details, and ClaimedBy contains an item_id foreign key, which connects from the Item details. 

### The updated ERD during completion/development of app
![Updated ERD](./docs/UpdatedERD.png)

Normalisation is a technique for database design which is used to organise tables in a way that reduces redundancy and dependency of data (North & Xu 2021). The main objective of normalisation is that a table is about a specific topic and only supporting topics are included, which minimizes duplicate data, avoids data modification issues, and simplifies queries (North & Xu 2021). I did aim to follow this logic with the Lost Property database, such as having the Staff table related to register/login purposes, the StaffProfile table for a few staff personal details, the Items table for the item details, and ClaimedBy to indicate who has claimed it and when. Early on, I thought of putting date_found and time_found in the "Found_By" table, but later thought these were more appropriate under Item details, and having EnteredBy/StaffProfile for more staff personal details. For a while I was wondering if there were any other attributes to add in StaffProfile, but couldn't think of anything else necessary or useful.

Implementing "unique=True" for attributes such as staff_email in Staff and email in ClaimedBy could assist with minimizing duplicate data, and help data integrity, ie. this data belonging only to that logged-in staff member. I also tried to use mostly unique attribute names in each model/table, ie. attribute names relevant to respective models/tables, also to avoid confusion and "Don't Repeat Yourself", such as "staff_name" under StaffProfile, "item_name" under Item, and "name" under ClaimedBy for the claimer's name, along with their contact details. However, I thought it would be helpful to record the date, ie. date_found and date_claimed in Item and ClaimedBy respectively, because it might useful for the item's owner to know "yes that would be mine", when approximately they left the item, and then to inform staff or customers when the item has been claimed, eg. if the owner needs to come and collect it later. I kept time, ie. time_found, only to Item.
 
Implementing "nullable=False" for some attributes, particularly in the Staff and StaffProfile tables, could also help prevent insertion anomalies, which can be a problem in non-normalized databases, the Staff table also being more vital for login/auth purposes. According to what I have read about the levels of normalizalization, the database for this app is likely to be at least 3NF, the third normal form, because "most 3NF relations are free of insertion, updation, and deletion anomalies" (Date 1999 and Wikipedia). Earlier in development and testing of this app, Postgres would give me error messages in the terminal if there were such anomalies or potential anomalies, such as "sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation) insert or update on table "staffprofiles" violates foreign key constraint "staffprofiles_staff_id_fkey"
DETAIL:  Key (staff_id)=(6) is not present in table "staffs".” So from my understanding, these anomalies are mostly cleared up now, for the app to function well, as indicated in Insomnia.

References:

Date, C. J. 1999. "An Introduction to Database Systems." Addison-Wesley Longman.

North, S & Xu, X 2021 "Introduction to Database Systems, 2nd Edition", Kennesaw State University, accessed 28 July 2024, https://alg.manifoldapp.org/read/introduction-to-database-systems/section/039a1438-ece4-4917-9596-254de7d52fd6#:~:text=Normalization%20is%20a%20technique%20in,all%20by%20using%20entity%20relationships.


## The implemented models and their relationships

This is how the models and their relationships were finally implemented, such as as I began to understand a bit more how they should be arranged, what to ultimately include and connect. And I kept in mind what staff/users and organisations would want from this app, and knowing the problem of lost property personally, having experienced it occasionally.

### Staff
#### Tablename: staffs
#### Attributes
* staff_id - an Integer, primary key (I probably should have put unique for this but forgot)
* organisation_name - a String which refers to the name of the organisation using this app
* staff_email - a String, a unique email address for each staff user, and not nullable
* staff_password - a String, a password for staff to access this app
* is_admin - Boolean, an admin status check upon authorisation, if the staff member/user is allocated as an admin, which might be relevant for managerial staff/users of this app

#### Associations
* staffprofile - one to many
* item - one to many
* claimedby - one to many

### StaffProfile
#### Tablename: staffprofiles
* staffprofile_id - an Integer, primary key
* staff_name - a String for the staff member's name, which is not nullable
* role - a String for the staff member's role or occupation in the organisation

* staff_id - an Integer, Foreign Key, ID of the staff/user entering their details into the StaffProfile fields, not nullable

#### Associations
* staff - one to one
* item - one to one

### Item
#### Tablename: items
* id - an Integer, primary key
* item_name - a String which refers to the name of an item such as ""Adidas T Shirt"
* description - a String for a brief description of the item, such as "black and white large"
* quantity - an Integer to indicate how many have been found of this item/s
* date_found - this will record the current date when a new item is entered, such as "2024-07-27"
* time_found - a String, which will be entered manually by staff. I looked into if there is a way to record or set the user/staff member's current time of entry, according to their timezone. For the time being, they'll enter time manually.
* location_found - a String to indicate where the item was found , such as "locker room under bench"
* now_claimed - a String, but staff/users can only enter VALID_STATUSES "Yes" or "No"

* staffprofile_id - an Integer, Foreign Key, ID of the staff profile entering details into Items, not nullable
* staff_id - an Integer, Foreign Key, ID of the staff/user entering details into Items, not nullable

#### Associations
* staffprofile - many to one
* staff - many to one
* claimedby - one to one

### ClaimedBy
#### Tablename: claimedbys
* id - an Integer, primary key  = db.Column(db.Integer, primary_key=True)
* name - a String for entering the name of the claimer
* phone - an Integer for the phone number of the claimer
* email - a String for the claimer's email address, which must be unique
* address - a String for the physical/home address of the claimer
* date_claimed - this will record the current date when a new claimedby is entered, such as "2024-07-28"

* item_id - an Integer, Foreign Key, ID of the item being claimed
* staff_id - an Integer, Foreign Key, ID of the staff/user entering details into ClaimedBy

#### Associations
* item - many to one
* staff - many to one


## Examples of how to use the API endpoints for the Lost Property API

### Staff
#### POST
/auth/register
![auth register1](./docs/API_images/authregister.png)
![auth register2](./docs/API_images/authregister2.png)

/auth/login
![auth login1](./docs/API_images/authlogin.png)
![auth login2](./docs/API_images/authlogin2.png)

For admin login:
![auth login3](./docs/API_images/authlogin_admin.png)

#### GET
To get all auth/staff details:
/auth/
![auth getall1](./docs/API_images/getall_authstaff.png)
![auth getall2](./docs/API_images/getall_authstaff2.png)

To get one auth/staff details:
/auth/staff/<int:staff_id>
![auth getone1](./docs/API_images/getone_authstaff.png)

#### PUT, PATCH
To update auth/staff details:
/auth/staff/<int:staff_id>
![auth update1](./docs/API_images/authstaff_update.png)
![auth update2](./docs/API_images/authstaff_update2.png)
![auth update3](./docs/API_images/authstaff_update3.png)

Only admin (logged in as admin) can update auth/staff details, including these of other staff in the organisation:
![auth update4](./docs/API_images/onlyadmin_updatestaff.png)

#### DELETE
To delete staff/auth details:
/auth/staff/<int:staff_id>
![auth delete1](./docs/API_images/authstaff_delete.png)

Only admin (logged in as admin) can delete auth/staff details, including these of other staff in the organisation:
![auth delete2](./docs/API_images/onlyadmin_deletestaff.png)

### StaffProfile
#### GET
To get all staffprofiles:
/staffprofile/
![staffprofile getall](./docs/API_images/getall_staffprofile.png)

To get one staffprofile:
/staffprofile/<int:staffprofile_id>
![staffprofile getone1](./docs/API_images/getone_staffprofile.png)
![staffprofile getone2](./docs/API_images/getone_staffprofile2.png)

#### POST
To enter new staffprofile:
/staffprofile/
![staffprofile new](./docs/API_images/newstaffprofile.png)

#### PUT, PATCH
To update staffprofile:
/staffprofile/<int:staffprofile_id>
![staffprofile update1](./docs/API_images/update_staffprofile.png)
![staffprofile update2](./docs/API_images/update_staffprofile2.png)

#### DELETE
To delete staffprofile:
/staffprofile/<int:staffprofile_id>
![staffprofile delete1](./docs/API_images/delete_staffprofile2.png)

### Item
#### GET
To get all items:
/item/
![item getall1](./docs/API_images/getallitem1.png)
![item getall2](./docs/API_images/getallitem2.png)

To get one item:
/item/<int:item_id>
![item getone](./docs/API_images/getone_item.png)

#### POST
To enter new item details:
/item/
![item new](./docs/API_images/newitem2.png)

#### PUT, PATCH
To update item details:
/item/<int:item_id>
![item update1](./docs/API_images/updateitem2.png)
![item update2](./docs/API_images/updateitem3.png)
![item update3](./docs/API_images/updateitem_patch.png)

Updating "now claimed":
![item update4](./docs/API_images/updateitem_now_claimed.png)

#### DELETE
To delete item details:
/item/<int:item_id>
![item delete1](./docs/API_images/deleteitem.png)

### ClaimedBy
#### GET
To get all claimedbys:
/claimedby/
![claimedby getall1](./docs/API_images/getall_claimedby.png)
![claimedby getall2](./docs/API_images/getall_claimedby2.png)

To get one claimedby:
/claimedby/<int:claimedby_id>
![claimedby getone](./docs/API_images/getone_claimedby.png)

#### POST
To enter new claimedby:
/claimedby/
![claimedby new](./docs/API_images/newclaimedby.png)

#### PUT, PATCH
To update claimedby:
/claimedby/<int:claimedby_id>
![claimedby update1](./docs/API_images/update_claimedby.png)
![claimedby update2](./docs/API_images/update_claimedby2.png)

#### DELETE
To delete claimedby:
/claimedby/<int:claimedby_id>
![claimedby delete](./docs/API_images/delete_claimedby2.png)

