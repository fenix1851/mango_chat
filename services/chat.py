from repository.chat import ChatRepository
from database.connections import get_database_connection

def get_chat_service() -> ChatRepository:
    db = get_database_connection()
    return ChatRepository(next(db))
