from flask import Flask, render_template_string, request, render_template
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
import os
import pymssql

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'different_key')

# CSRF Protection
csrf = CSRFProtect(app)

# Content Security Policy and Clickjacking Protection
Talisman(
    app,
    content_security_policy={
        'default-src': "'self'",
        'style-src': "'self' 'unsafe-inline'",
        'script-src': "'self' 'unsafe-inline'",
        'img-src': "'self'",
        'font-src': "'self'",
        'frame-ancestors': "'none'"
    },
    frame_options='SAMEORIGIN',
    strict_transport_security=True
)

# Database connection


def get_db_connection():
    username = "yassine"
    password = os.environ.get("AZURE_SQL_PASSWORD")
    server = "asesql2.database.windows.net"
    database = "ase_sql"
    return pymssql.connect(server, username, password, database)

# Error handling


@app.errorhandler(500)
def internal_server_error(e):
    return render_template_string('<h1>Internal Server Error</h1>'), 500

# Routes


@app.route('/')
def index():
    return render_template_string(open('templates/index.html').read())


# ...

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        age = request.form['age']
        print(f"Received name: {name}, age: {age}")

        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_info (name, age) VALUES (%s, %s)", (name, age))
        conn.commit()
        cursor.close()
        conn.close()

        # Show confirmation message
        confirmation_message = f'Thank you, {name}! Your information has been submitted successfully.'

        return render_template_string(f'''
            <h1>{confirmation_message}</h1>
            <button onclick="window.location.href='/view-users'">View All Users</button>
        ''')
    except Exception as e:
        print(f"Error during submission: {e}")
        error_message = 'An error occurred during submission. Please try again.'
        return render_template_string(f'<h1>{error_message}</h1>'), 500

# ...


@app.route('/view-users')
def view_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_info")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('database.html', users=users)


if __name__ == '__main__':
    app.run()
