from flask import Blueprint, render_template
import psycopg2
from dotenv import load_dotenv
import os
from .backend import format

views = Blueprint('views', __name__)

load_dotenv()

db_url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(db_url)


@views.route('/')
def home():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO analytics (page, visit_time) VALUES ('home', CURRENT_TIMESTAMP);")

            cursor.execute("SELECT * FROM hof WHERE category = 'skills' ORDER BY title_id;")
            vals = cursor.fetchall()

            connection.commit()

            res = format.db_response(vals)

    return render_template("home.html", skills=res)


@views.route('/slayer')
def slayer():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO analytics (page, visit_time) VALUES ('slayer', CURRENT_TIMESTAMP);")

            cursor.execute("SELECT * FROM hof WHERE category = 'slayer' ORDER BY title_id;")
            vals = cursor.fetchall()

            connection.commit()

            res = format.db_response(vals)

    return render_template("home.html", skills=res)


@views.route('/misc')
def misc():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO analytics (page, visit_time) VALUES ('misc', CURRENT_TIMESTAMP);")

            cursor.execute("SELECT * FROM hof WHERE category = 'misc' ORDER BY title_id;")
            vals = cursor.fetchall()

            connection.commit()

            res = format.db_response(vals)

    return render_template("home.html", skills=res)


@views.route('/blacklist')
def blacklist():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO analytics (page, visit_time) VALUES ('blacklist', CURRENT_TIMESTAMP);")

            cursor.execute("SELECT * FROM blacklist ORDER BY list_id;")

            connection.commit()

            vals = cursor.fetchall()

    return render_template("blacklist.html", vals=vals)


@views.route('/update')
def update():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO analytics (page, visit_time) VALUES ('update', CURRENT_TIMESTAMP);")
            connection.commit()

    return render_template("update_data.html")
