release: sh -c 'cd src && python manage.py migrate'
web: gunicorn --pythonpath src swindle.wsgi