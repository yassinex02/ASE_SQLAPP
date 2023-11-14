from flask import Flask, render_template, request, redirect
import pymssql
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Function to get a database connection


def get_db_connection():
    username = "yassine"
    password = os.environ.get("AZURE_SQL_PASSWORD")
    server = "asesql2.database.windows.net"
    database = "ase_sql"
    return pymssql.connect(server, username, password, database)

# Function to create the user_info table if not exists


def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='user_info' and xtype='U')
        CREATE TABLE user_info (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name VARCHAR(255),
            age INT
        )
    ''')
    conn.commit()
    cursor.close()

# Function to insert user data into the user_info table


def insert_user_data(conn, name, age):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_info (name, age) VALUES (%s, %s); SELECT SCOPE_IDENTITY()", (name, age))
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return new_id

# Function to query and fetch all data from the user_info table


def query_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_info")
    data = cursor.fetchall()
    cursor.close()
    return data

# Route for the home page with buttons


@app.route('/')
def home():
    return render_template('home.html')

# Route to handle form submission


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']

    conn = get_db_connection()
    insert_user_data(conn, name, age)
    conn.close()

    return redirect('/')

# Route to show the user info table


@app.route('/show-database')
def show_database():
    conn = get_db_connection()
    create_table_if_not_exists(conn)
    data = query_all_data(conn)
    conn.close()
    return render_template('database.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
