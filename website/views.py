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

            cursor.execute("SELECT * FROM hof WHERE category = 'skyblock' ORDER BY title_id;")
            vals = cursor.fetchall()

            connection.commit()

            res = format.db_response(vals)

    return render_template("category.html", skills=res)


@views.route('/lb/<category>')
def slayer(category):
    with connection:
        with connection.cursor() as cursor:

            category = category.lower()

            cursor.execute(f"INSERT INTO analytics (page, visit_time) VALUES ('{category}', CURRENT_TIMESTAMP);")

            cursor.execute(f"SELECT * FROM hof WHERE category = '{category}' ORDER BY title_id;")
            vals = cursor.fetchall()

            connection.commit()

            res = format.db_response(vals)

    return render_template("category.html", skills=res)


@views.route('/blacklist')
def blacklist():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO analytics (page, visit_time) VALUES ('blacklist', CURRENT_TIMESTAMP);")

            cursor.execute("SELECT * FROM blacklist ORDER BY p_id;")

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
