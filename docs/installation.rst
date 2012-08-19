============
Installation
============

Clone the repo
--------------

    git clone git://github.com/reinbach/tutorus.git

Create VirtualEnv
-----------------

    mkvirtualenv tutorus

Install requirements
--------------------

    pip install -r requirements.txt

Configure settings
------------------

Configure your settings ``settings/<env>.py`` and then create symlink back to <env>.py called ``currentenv.py``

    ln -s settings/prod.py settings/currentenv.py
    
Sync Database
-------------
    
    python manage.py syncdb
    
Run migrations
--------------

    python manage.py migrate

Collect Static Media
--------------------

    python manage.py collectstatic

Start Server
------------
Start server <dev mode>

    python manage.py collectstatic
    
    
Running the unit tests
----------------------

    ./manage test --settings=settings.test
    
Making the Docs
---------------
    
    cd docs
    make html