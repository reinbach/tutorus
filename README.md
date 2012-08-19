TutorUs
=======

Team FryMe's entry in the Django Dash 2012 competition

Setup/Installation
==================

pip install -r requirements.txt

Install Postgres
================

For a quick install on Mac OS X install postgres from: http://postgresapp.com/

Create a local settings file
============================

copy one of the settings files in the `tutorus/tutorus/settings` to a new file

Setup the database
==================

./manage syncdb --settings=settings.john
./manage migrate --settings=settings.john


Starting the application
========================

./manage runserver --settings=settings.john

Running the unit tests
======================

./manage test --settings=settings.test