from flask import Flask, render_template, request, redirect, url_for
import pymssql
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Function to establish a database connection


def get_db_connection():
    username = "yassine"
    password = os.environ.get("AZURE_SQL_PASSWORD")
    server = "asesql2.database.windows.net"  # change to your server
    database = "ase_sql"
    return pymssql.connect(server, username, password, database)

# Function to create the user_info table if it doesn't exist


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


# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']

    # Insert data into the database
    conn = get_db_connection()
    create_table_if_not_exists(conn)
    insert_data(conn, name, age)
    conn.close()

    return redirect(url_for('home'))

# Route for displaying all data


@app.route('/show_database')
def show_database():
    # Fetch all data from the database
    conn = get_db_connection()
    data = query_all_data(conn)
    conn.close()

    return render_template('show_database.html', data=data)


if __name__ == '__main__':
    app.run(debug=False)
