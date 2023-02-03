from loguru import logger

class UserWithPhoneAlreadyExistsException(Exception):
    logger.error(f"User with phone already exists")
    pass

class NotValidPhotoException(Exception):
    logger.error(f"Photo not valid")
    pass

class IncorrectPasswordException(Exception):
    logger.error(f"Incorrect password")
    pass

class AccessDeniedException(Exception):
    logger.error(f"Access denied")
    pass


class ChatAlreadyExistsException(Exception):
    logger.error(f"Chat already exists")
    pass