# Parts Warehouse API
Flask, MongoDB API involving management of Parts and categories they belong to
in a theoretical warehouse.


## Features
- Uses Flask, MongoEngine, Pytest, Docker, marshmallow
- Validation of request fields, with additional checks on deletion of categories
  and category name of part.
- Unit tests with mocks used when needed

## Assumptions
There are some assumptions I made while developing the project
- MongoDB collections don't have enforced structure unlike in relational DBs
  While there are specific checks for validation conditions, required fields, it is possible 
  to add your own fields in Part and Category models, by adding the field in request body. 
  Location embedded document is exception, where it was not possible to allow unknown fields.
- Location parameters are assumed to described by numbers - Xth row, Yth shelf, Zth room etc.
- Separate local db is used for tests and separate db for normal use.
- "Production" settings assume connection to remote database 
- Category with blank parent_name is base category. Only names of base or other subcategories
  can be used by Parts when assigning category they belong to


## Installation and use
1. Create .env file using example and set required values.
    - Mode can be 'development' or 'production'. Application uses different settings in each mode.
    - MONGODB_DB_NAME is a name of main local database
2. Build and install the project by running commands:
```
Docker compose build
Docker compose up
```
3. Generate basic data using command
  ```
  make generate_data
  ```

Additional utility commands, can be found in makefile.


### Tests
Run tests with command:
```
make test
```


## Endpoint documentation
Check `/docs/swagger/`` for the documentation


### Search endpoint
Search GET endpoint takes query parameters of Part fields, and allows to search using them as input data.