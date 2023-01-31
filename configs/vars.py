from starlette.config import Config

config = Config('.env')

POSTGRES_USER = config("POSTGRES_USER")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
POSTGRES_HOST = config("POSTGRES_HOST")
POSTGRES_PORT = config("POSTGRES_PORT")
POSTGRES_DB = config("POSTGRES_DB")
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:" \
               f"{POSTGRES_PORT}/{POSTGRES_DB}"
SALT = config("SALT")
