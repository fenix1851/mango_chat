from database.session import SessionLocal


def get_database_connection():
    try:
        db = SessionLocal()
        yield db
        print('Connected to db')
    finally:
        db.close()