import os
import pymssql

# Get the connection details from the environment variables

password = os.environ.get("AZURE_SQL_PASSWORD")

# %%


def get_db_connection():
    username = "yassine"
    password = "Ihatemylifelol#75"
    server = "asesql2.database.windows.net"

    database = "ase_sql"

    return pymssql.connect(server, username, password, database)


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


def insert_dummy_data(conn):

    cursor = conn.cursor()

    cursor.execute("INSERT INTO user_info (name, age) VALUES ('John', 30)")

    cursor.execute("INSERT INTO user_info (name, age) VALUES ('Jane', 25)")

    conn.commit()

    cursor.close()


def query_and_print(conn, query):

    cursor = conn.cursor()

    cursor.execute(query)

    for row in cursor:

        print(row)

    cursor.close()


create_table_if_not_exists(get_db_connection())

insert_dummy_data(get_db_connection())

query_and_print(get_db_connection(), "SELECT * FROM user_info")
