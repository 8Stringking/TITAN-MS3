from flask import render_template, request, redirect, url_for
from titanportal import app, db
from titanportal.models import Department, Colleague


@app.route("/")
def home():
    return render_template("colleagues.html")


@app.route("/departments")
def departments():
    departments = list(Department.query.order_by(Department.department_name).all())
    return render_template("departments.html", departments=departments)


@app.route("/add_department", methods=["GET", "POST"])
def add_department():
    if request.method == "POST":
        department = Department(
            department_name=request.form.get("department_name"))
        db.session.add(department)
        db.session.commit()
        return redirect(url_for("departments"))
    return render_template("add_department.html")


@app.route("/edit_department/<int:department_id>", methods=["GET", "POST"])
def edit_department(department_id):
    department = Department.query.get_or_404(department_id)
    if request.method == "POST":
        department.department_name = request.form.get("department_name")
        db.session.commit()
        return redirect(url_for("departments"))
    return render_template("edit_department.html", department=department)


@app.route("/delete_department/<int:department_id>")
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()
    return redirect(url_for("departments"))
