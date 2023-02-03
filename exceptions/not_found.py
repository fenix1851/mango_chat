from loguru import logger

class UserNotFoundException(Exception):
    logger.error("User not found")
    pass


class ChatNotFoundException(Exception):
    logger.error(f"Chat not found")
    pass

class MessageNotFoundException(Exception):
    logger.error(f"Message not found")
    pass

class MessageTypeNotFoundException(Exception):
    logger.error(f"Message type not found")
    pass


class RefreshTokenNotFoundException(Exception):
    logger.error(f"Refresh token not found")
    pass
