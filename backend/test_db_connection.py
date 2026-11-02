from sqlalchemy import text
from database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), current_user, version()")
        )
        print("Database connection successful!")
        print(result.fetchone())

except Exception as error:
    print("Database connection failed!")
    print(type(error).__name__, error)