from flask import render_template
from titanportal import app, db
from titanportal.models import Department, Colleague


@app.route("/")
def home():
    return render_template("base.html")
