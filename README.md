

### Instructions

#### 1. Clone the project:

    $ git clone https://github.com/marcromeyn/ottomen.git
    $ cd ottomen

#### 2. Build and get the images with Docker-Compose:

    $ docker-compose build
    $ docker-compose up -d
    
#### 3. Upgrade the database:

    $ docker-compose run web python manage.py db upgrade
    
#### 4. Seed the database:

    $ docker-compose run web python manage.py db seed
    
#### 5. Run the development server:

    $ docker-compose up


#### Management Commands

Management commands can be listed with the following command:

    $ python manage.py

These can sometimes be useful to manipulate data while debugging in the browser.    


#### Database Migrations

To create a database migration, run the following command:

    $ python manage.py db migrate
    
Then run the upgrade command

    $ python manage.py db upgrade


#### Tests

To run the tests use the following command:

    $ nosetests
