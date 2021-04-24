# Swindle Leaderboards

## Setting up the project

Our python dependencies are listed in `requirements.txt`.

We use `django-environ` to manage secrets and configuration. Before getting
started, you'll want to bootstrap your environment:

```
cp src/.env.example src/.env
```

Feel free to edit the values in `src/.env` to your liking, this file is
versioned.

Now, you may either launch the app with Docker or python (3):

```
docker-compose up

# Or

cd src
python manage.py runserver
```

## License

MIT