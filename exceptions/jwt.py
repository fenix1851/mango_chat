from loguru import logger

class InvalidTokenException(Exception):
    logger.error(f"Invalid token")
    pass

class TokenExpiredException(Exception):
    logger.error(f"Token expired")
    pass
