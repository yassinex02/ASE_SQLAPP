import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from the file
load_dotenv(".env")

# Get the connection string from the environment variables
connection_string = os.environ.get("AZURE_SQL_CONNECTIONSTRING")


def create_table():
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Create a table with columns Name (string) and Age (integer)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserData (
                ID INT IDENTITY(1,1) PRIMARY KEY,
                Name NVARCHAR(255),
                Age INT
            );
        """)

        conn.commit()
        print("Table created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    create_table()
