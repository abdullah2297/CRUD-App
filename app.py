from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import pyodbc
from flask import g


import urllib

app = Flask(__name__)

app.secret_key = 'Secret Key'
params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-2BVV9CV;DATABASE=crud;Trusted_Connection=yes;')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone 


@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template("index.html", my_data = all_data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        mydata = Data(name, email, phone)
        db.session.add(mydata)
        db.session.commit()
        flash('Inserted successfully')
        return redirect(url_for('index'))

@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        mydata = Data.query.get(request.form.get('id'))

        mydata.name = request.form['name']
        mydata.email =request.form['email']
        mydata.phone =request.form['phone']

        db.session.commit()
        return redirect(url_for('index'))
    
@app.route('/delete/<id>', methods = ['GET', 'POST'])
def delete(id):
        mydata = Data.query.get(id)
        db.session.delete(mydata)
        db.session.commit()
        return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
