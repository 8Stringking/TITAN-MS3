from flask import render_template, flash, request, session, redirect, url_for
from titanportal import app, db
from titanportal.models import Department, Colleague


@app.route("/")
def home():
    colleagues = list(Colleague.query.order_by(Colleague.id).all())
    return render_template("colleagues.html", colleagues=colleagues)


@app.route("/departments")
def departments():
    departments = list(Department.query.order_by(
        Department.department_name).all())
    return render_template("departments.html", departments=departments)


@app.route("/add_department", methods=["GET", "POST"])
def add_department():
    if request.method == "POST":
        department = Department(
            department_name=request.form.get("department_name"))
        db.session.add(department)
        db.session.commit()
        flash("New Department Added")
        return redirect(url_for("departments"))
    return render_template("add_department.html")


@app.route("/edit_department/<int:department_id>", methods=["GET", "POST"])
def edit_department(department_id):
    department = Department.query.get_or_404(department_id)
    if request.method == "POST":
        department.department_name = request.form.get("department_name")
        db.session.commit()
        flash("Department Successfully Edited")
        return redirect(url_for("departments"))
    return render_template("edit_department.html", department=department)


@app.route("/delete_department/<int:department_id>")
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()
    flash("Department Successfully Deleted")
    return redirect(url_for("departments"))


@app.route("/add_colleague", methods=["GET", "POST"])
def add_colleague():
    departments = list(Department.query.order_by(
        Department.department_name).all())
    if request.method == "POST":
        colleague = Colleague(
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
            role=request.form.get("role"),
            department_id=request.form.get("department_id")
        )
        db.session.add(colleague)
        db.session.commit()
        flash("Colleague Successfully Added")
        return redirect(url_for("home"))
    return render_template("add_colleague.html", departments=departments)


@app.route("/edit_colleague/<int:colleague_id>", methods=["GET", "POST"])
def edit_colleague(colleague_id):
    colleague = Colleague.query.get_or_404(colleague_id)
    departments = list(Department.query.order_by(
        Department.department_name).all())
    if request.method == "POST":
        colleague.first_name = request.form.get("first_name"),
        colleague.last_name = request.form.get("last_name"),
        colleague.role = request.form.get("role"),
        colleague.department_id = request.form.get("department_id")
        db.session.commit()
        flash("Colleague Successfully Edited")
        return redirect(url_for("home"))
    return render_template("edit_colleague.html", colleague=colleague, departments=departments)


@app.route("/delete_colleague/<int:colleague_id>")
def delete_colleague(colleague_id):
    colleague = Colleague.query.get_or_404(colleague_id)
    db.session.delete(colleague)
    db.session.commit()
    flash("Colleague Successfully Deleted")
    return redirect(url_for("home"))


# @app.route("/colleague_search/<int:colleague_id>", methods=["GET", "POST"])
# def colleague_search(colleague_id):
    # colleague = Colleague.query.get_or_404(colleague_id)
    # if request.method == "POST":
        # colleague.query.filter_by(colleague.colleague_id, colleague.first_name, colleague.last_name, colleague.department_id)
    # return render_template("colleagues.html", colleagues=colleagues)
