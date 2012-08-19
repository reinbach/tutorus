============
Installation
============

Clone the repo

    git clone git://github.com/reinbach/tutorus.git

Create VirtualEnv

    mkvirtualenv tutorus

Install requirements

    pip install -r requirements.txt
    
Configure your settings ``settings/<env>.py`` and then create symlink back to <env>.py called ``currentenv.py``

    ln -s settings/prod.py settings/currentenv.py
    
Run syncdb
    
    python manage.py syncdb
    
Run migrations

    python manage.py migrate
    
Collect static media

    python manage.py collectstatic
    
Start server <dev mode>

    python manage.py collectstatic