from flask import Blueprint, render_template
import psycopg2
from dotenv import load_dotenv
import os

views = Blueprint('views', __name__)

load_dotenv()

db_url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(db_url)


@views.route('/')
def home():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM hof WHERE category = 'skills' ORDER BY title_id;")
            vals = cursor.fetchall()

            res = []

            for val in vals:
                res.append([val[0], val[1], val[2], val[3], val[4], '{0:,}'.format(val[5]),
                            val[6], '{0:,}'.format(val[7]), val[8], '{0:,}'.format(val[9])])

    return render_template("home.html", skills=res)


@views.route('/update')
def update():
    return render_template("update_data.html")
