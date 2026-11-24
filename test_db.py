from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:@localhost:3307/fastapi_db"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        print("MySQL connected successfully!")
        print(result.scalar())

except Exception as error:
    print("Database connection failed:",)