# Software Project

## Development

### Using Flask

Add these files at root folder with the following content:

```
# .env

SECRET_KEY=cdc1db14963d4ba7684fa7fd4b74c417
```

```
# .flaskenv

FLASK_APP=app.py
FLASK_DEBUG=TRUE
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
```

**Run app**

```bash
$ pip install -r requirements.txt
$ flask run
```

Remember to user a python virtual environment before installing.

### Using Docker Compose

This requires to have docker and docker-compose installed

**Run app**

```
$ docker-compose up --build -d
```

**Stop app**

```
$ docker-compose down -v
```