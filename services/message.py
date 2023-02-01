from repository.message import MessageRepository
from database.connections import get_database_connection


def get_message_service() -> MessageRepository:
    db = get_database_connection()
    return MessageRepository(next(db))
