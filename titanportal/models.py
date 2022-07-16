from titanportal import db


class Department(db.Model):
    # schema for the department model
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(20), nullable=False)
    colleagues = db.relationship(
        "Colleague", backref="department", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself inform of a string
        return self.department_name


class Colleague(db.Model):
    # schema for the colleague model
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(15), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
            "department.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself inform of a string
        return f"#{self.id}-First:{self.first_name}|Last:{self.last_name}"
