from repository.user import UserRepository
from database.connections import get_database_connection


def get_user_service() -> UserRepository:
    db = get_database_connection()
    return UserRepository(next(db))
