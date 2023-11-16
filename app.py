from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flaskaws'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:P!ATD2001@flaskaws.c9789jpe9v1g.eu-west-1.rds.amazonaws.com/flaskaws'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "somethingunique"

db = SQLAlchemy(app)


class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(100), nullable = False)

    def __init__(self, name, role):
        self.name = name
        self.role = role
        

@app.route('/')

def index():
    members = Member.query.all()
    return render_template('index.html', members=members)


@app.route('/add/', methods = ['POST'])

def insert_member():
    if request.method =="POST":
        member = Member(
            name = request.form.get('name'),
            role = request.form.get('role'),
        )
        db.session.add(member)
        db.session.commit()
        flash("Member added successfully")
        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods = ['GET', 'POST'])

def delete(id):
    my_data = Member.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Member has been deleted")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug = True)
