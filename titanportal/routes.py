from flask import render_template, flash, request, session, redirect, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from titanportal import app, db, mongo
from titanportal.models import Department, Colleague


# this route is the default page for the app that displays the index page
@app.route("/")
def home():
    return render_template("index.html")


# this route is for logging into the app
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")
            ):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("colleague_search", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("index.html")


# the route for logging out
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# route for registering
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # checks if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("home", username=session["user"]))

    return render_template("register.html")


# this renders the colleague search page and retrieves the
# colleague info from the database
@app.route("/colleague_search")
def colleague_search():
    colleagues = list(Colleague.query.order_by(Colleague.id).all())
    return render_template("colleagues.html", colleagues=colleagues)


# this renders the department page and retrieves created departments
# from the database
@app.route("/departments")
def departments():
    departments = list(Department.query.order_by(Department.department_name).all())
    return render_template("departments.html", departments=departments)


# this adds a department to the database but ensuring only admin user can do this
@app.route("/add_department", methods=["GET", "POST"])
def add_department():

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage departments!")
        return redirect(url_for("departments"))

    if request.method == "POST":
        department = Department(department_name=request.form.get("department_name"))
        db.session.add(department)
        db.session.commit()
        flash("New Department Added")
        return redirect(url_for("departments"))
    return render_template("add_department.html")


# this edits a department in the database but ensuring only admin user can do this
@app.route("/edit_department/<int:department_id>", methods=["GET", "POST"])
def edit_department(department_id):

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage departments!")
        return redirect(url_for("departments"))

    department = Department.query.get_or_404(department_id)
    if request.method == "POST":
        department.department_name = request.form.get("department_name")
        db.session.commit()
        flash("Department Successfully Edited")
        return redirect(url_for("departments"))
    return render_template("edit_department.html", department=department)


# this deletes a department from the database and only lets admin user do this
@app.route("/delete_department/<int:department_id>")
def delete_department(department_id):

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage departments!")
        return redirect(url_for("departments"))

    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()
    flash("Department Successfully Deleted")
    return redirect(url_for("departments"))


# this adds a colleague to the database but ensuring only admin user can do this
@app.route("/add_colleague", methods=["GET", "POST"])
def add_colleague():

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to add colleagues!")
        return redirect(url_for("colleague_search"))

    departments = list(Department.query.order_by(Department.department_name).all())
    if request.method == "POST":
        colleague = Colleague(
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
            role=request.form.get("role"),
            department_id=request.form.get("department_id"),
        )
        db.session.add(colleague)
        db.session.commit()
        flash("Colleague Successfully Added")
        return redirect(url_for("colleague_search"))
    return render_template("add_colleague.html", departments=departments)


# this edits a colleague to the database but ensuring only admin user can do this
@app.route("/edit_colleague/<int:colleague_id>", methods=["GET", "POST"])
def edit_colleague(colleague_id):

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to edit colleagues!")
        return redirect(url_for("colleague_search"))

    colleague = Colleague.query.get_or_404(colleague_id)
    departments = list(Department.query.order_by(Department.department_name).all())
    if request.method == "POST":
        colleague.first_name = (request.form.get("first_name"),)
        colleague.last_name = (request.form.get("last_name"),)
        colleague.role = (request.form.get("role"),)
        colleague.department_id = request.form.get("department_id")
        db.session.commit()
        flash("Colleague Successfully Edited")
        return redirect(url_for("colleague_search"))
    return render_template(
        "edit_colleague.html", colleague=colleague, departments=departments
    )


# this deletes a colleague from the database and only lets admin user do this
@app.route("/delete_colleague/<int:colleague_id>")
def delete_colleague(colleague_id):

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to delete colleagues!")
        return redirect(url_for("colleague_search"))

    colleague = Colleague.query.get_or_404(colleague_id)
    db.session.delete(colleague)
    db.session.commit()
    flash("Colleague Successfully Deleted")
    return redirect(url_for("colleague_search"))


# this retrieves all data from mongo db and presents them in list form
@app.route("/get_associate")
def get_associate():
    associate = list(mongo.db.associate.find())
    return render_template("personal_info.html", associate=associate)


# this adds personal information to the database but ensuring only admin user can do this
@app.route("/add_associate", methods=["GET", "POST"])
def add_associate():

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to add personal information!")
        return redirect(url_for("get_associate"))

    if request.method == "POST":
        associate = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "colleague_number": request.form.get("colleague_number"),
            "department": request.form.get("department"),
            "role": request.form.get("role"),
            "contact": request.form.get("contact"),
            "date_of_birth": request.form.get("date_of_birth"),
        }
        mongo.db.associate.insert_one(associate)
        flash("Personal Information Successfully Added")
        return redirect(url_for("get_associate"))

    return render_template("add_personal_info.html")


# this edits personal information in the database but ensuring only admin user can do this
@app.route("/edit_associate/<associate_id>", methods=["GET", "POST"])
def edit_associate(associate_id):

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to edit personal information!")
        return redirect(url_for("get_associate"))

    if request.method == "POST":
        submit = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "colleague_number": request.form.get("colleague_number"),
            "department": request.form.get("department"),
            "role": request.form.get("role"),
            "contact": request.form.get("contact"),
            "date_of_birth": request.form.get("date_of_birth"),
        }
        mongo.db.associate.update_one({"_id": ObjectId(associate_id)}, {"$set": submit})
        flash("Personal Information Successfully Updated")
        return redirect(url_for("get_associate"))

    associate = mongo.db.associate.find_one({"_id": ObjectId(associate_id)})
    return render_template("edit_personal_info.html", associate=associate)


# this deletes personal information in the database but ensuring only admin user can do this
@app.route("/delete_associate/<associate_id>")
def delete_associate(associate_id):

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to delete personal information!")
        return redirect(url_for("get_associate"))

    mongo.db.associate.delete_one({"_id": ObjectId(associate_id)})
    flash("Personal Information Successfully Deleted")
    return redirect(url_for("get_associate"))


# this route is for the search functionality for the mongodb and presents them as a list
@app.route("/search_info", methods=["GET", "POST"])
def search_info():
    query = request.form.get("query")
    associate = list(mongo.db.associate.find({"$text": {"$search": query}}))
    return render_template("personal_info.html", associate=associate)
