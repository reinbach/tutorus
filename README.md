TutorUs
=======

Team FryMe's entry in the Django Dash 2012 competition.  The source code can be found here: https://github.com/reinbach/tutorus

Authors
=======
- Greg Reinbach
- John Costa
- Ken Cochrane

Documentation
=============
Just like all the cool projects, we are on Read the Docs. http://tutorus.readthedocs.org


Demo Site
=========

A demo of the application can be found here: http://rocky-brook-2492.herokuapp.com/

Setup/Installation
==================

Clone the repo
--------------

    git clone git://github.com/reinbach/tutorus.git

Create VirtualEnv
-----------------

    mkvirtualenv tutorus

    pip install -r requirements.txt

Install Postgres
----------------

For a quick install on Mac OS X install postgres from: http://postgresapp.com/

Create a local settings file
----------------------------

copy one of the settings files in the `tutorus/tutorus/settings` to a new file

Setup the database
------------------

    ./manage syncdb --settings=settings.john
    ./manage migrate --settings=settings.john


Starting the application
------------------------

    ./manage runserver --settings=settings.john

Running the unit tests
----------------------

    ./manage test --settings=settings.test
    
Making the Docs
---------------
    
    cd docs
    make html