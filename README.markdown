# Basin web

Setup:

    python3.4 -mvenv venv
    venv/bin/pip install https://www.djangoproject.com/download/1.7b3/tarball/
    venv/bin/pip install -r requirements.txt
    venv/bin/python manage.py migrate

Run:

    venv/bin/python manage.py runserver

states:

- active
- sleeping
- blocked
- delegated
- completed
- trashed
