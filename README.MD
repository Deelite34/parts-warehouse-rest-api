# Parts Warehouse API
Flask, MongoDB API involving management of Parts and categories they belong to
in a theoretical warehouse.


## Features
- Uses Flask, MongoEngine, Marshmallow, Pytest, Docker to create CRUD api
- Validation of request fields, with additional checks on deletion of categories
  and category name of part.
- Pytest unit tests with mocks used when needed
- Linting, formatting with Ruff

## Assumptions, notes
There are some assumptions I made while developing the project
- Why flask? - My alternative option for his project was Django. Django is batteries included framework,
  that would be great choice, if I needed the required batteries. Django ORM does not support MongoDB,
  I had no need for admin panel. Instead of stripping house called django, it was easier for me to build up from scratch a 
  flask app where I would choose api framework, serialization/deserialization and orm/mongodb libraries better suited for my needs of this project.
  Besides that, I have been learning flask for a while, and it was a good chance to experiment with new libraries.

- MongoDB collections don't have enforced structure unlike in relational DBs
  While there are specific checks for validation conditions, required fields, it is possible 
  to add your own fields in Part and Category models, by adding the field in request body. 
  Location embedded document is exception, where it was not possible to allow unknown fields.

- Location parameters are assumed to described by numbers - Xth row, Yth shelf, Zth room etc.

- Settings allow use of local databases "test" database for tests, separate db for development use and remote theoretical production database.

- "Production" settings use connection to remote database 

- Category with blank parent_name is base category. Only names of base or other subcategories
  can be used by Parts when assigning category they belong to

- Learned new technologies: MongoDB, MongoEngine, Ruff, Flask-Smorest


## Installation and use
1. Run command `git clone git@github.com:Deelite34/parts-warehouse-rest-api.git`
2. Run command `cd parts-warehouse-rest-api`
3. Create `.env` file using `example.env` file as base and set required and described values. 
4. Build and install the project by running commands:
```
Docker compose build
Docker compose up
```
5. Generate sample data consisting of base category, 3 subcategories, 6 parts assigned to random subcategories using command:
  ```
  make generate_data
  ```

Additional utility commands, can be found in makefile.


## Endpoint documentation
Check `/docs/swagger/` route for the documentation of API.  
Search GET endpoint takes query parameters of Part fields, and allows to search using them as input data.


### Tests
Pytest tests can be run using command
```
make test
```
