# T2A2_Lost_property_API

## How to Set Up

python3 -m flask db drop && python3 -m flask db create && python3 -m flask db seed
flask run
## Purpose and Aim

## How tasks are allocated and tracked

## The third-party services, packages and dependencies used in this app

## The benefits and drawbacks of this app’s underlying database system
Benefits of using Postgres include (IONOS 2022):
- Open source, ie. free to use.
- Highly expandable, eg. unlimited number of rows and unlimited number of indexes.
- Supporting JSON, which has been ideal for this project, such as for testing the API.
- It is possible to process complex data types (e.g. geographical data). It does process the current date for instance, as in the ClaimedBy and Item tables.
- Ability for flexible full text search.

One noticeable disadvantage of Postgres so far (at least indicatd in the terminal), is not being able to properly implement the phone number field for the claimedby table, eg. for phone numbers starting with 0, such as 0200010110. If I tried to enter a phone number beginning with 0 in Insomnia, I got an error message such as:
"SyntaxError: leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers".
This system didn't seem to accept numbers, such as phone numbers, beginning with 0. In future, to get around this, I might recommend that staff/users enter these phone numbers without beginning zeros where possible. Also, I was unable to properly implement a minimum and maximum for the phone number field, intended to be between 6 and 10 numbers. I further explained this in comments on my Trello board.

Other disadvantages of Postgres include a comparatively low reading speed and not being available on all hosts by default (IONOS 2022).

Reference:
IONOS 2022, "PostgreSQL: a closer look at the object-relational database management system", IONOS, accessed 28 July 2024, https://www.ionos.com/digitalguide/server/know-how/postgresql/


## The features, purpose and functionalities of the ORM used in this app
(Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.)

## The entity relationship diagram (ERD) for this app’s database

 The draft I designed, as I understood it early on and during coding, developing/writing the models and controllers.

(explain how the relations between the diagrammed models will aid the database design. 

This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase.)

## The implemented models and their relationships

(including how the relationships aid the database implementation)
(This should focus on the database implementation AFTER coding has begun, eg. during the project development phase.)

## How to use the API endpoints for the Lost Property API


(screenshots)
(HTTP verb
Path or route
Any required body or header data
Response)

