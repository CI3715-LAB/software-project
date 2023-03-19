FROM python:3.10.9-bullseye

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV FLASK_APP=app.py

ENV FLASK_DEBUG=True

ENV FLASK_RUN_HOST=0.0.0.0

ENV FLASK_RUN_PORT=5000

ENV SECRET_KEY=cdc1db14963d4ba7684fa7fd4b74c417

EXPOSE 5000:5000

CMD ["flask", "run"]

#RUN sqlite3 ./instance/sqlite.db < init.sql