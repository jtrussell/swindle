release: sh -c 'cd src && python manage.py migrate'
web: bin/start-nginx gunicorn -c config/gunicorn.conf.py --pythonpath src swindle.wsgi