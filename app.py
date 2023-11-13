from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Set your Azure SQL Database credentials as environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from azure import identity
import pyodbc
import struct

load_dotenv(".env")  # Load environment variables from the file


# Get the connection string from the environment variables
connection_string = os.environ.get("AZURE_SQL_CONNECTIONSTRING")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    age = request.form['age']

    new_user = User(name=name, age=age)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
