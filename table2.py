import pymssql
import os
from dotenv import load_dotenv

# Load environment variables from the file
load_dotenv(".env")

# Get the connection details from the environment variables
server = os.environ.get("AZURE_SQL_SERVER")
user = os.environ.get("AZURE_SQL_USERNAME")
password = os.environ.get("AZURE_SQL_PASSWORD")
database = os.environ.get("AZURE_SQL_DATABASE")

# Construct the connection string
connection_string = f"server={server}, user={user}, password={password}, database={database}"


def create_table():
    conn = None
    try:
        conn = pymssql.connect(connection_string)
        cursor = conn.cursor()

        # Create a table with columns Name (string) and Age (integer)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserData (
                ID INT IDENTITY(1,1) PRIMARY KEY,
                Name NVARCHAR(255),
                Age INT
            )
        """)

        conn.commit()
        print("Table created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_table()
