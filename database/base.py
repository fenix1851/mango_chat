from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from configs.vars import DATABASE_URL
from sqlalchemy.pool import NullPool

engine = create_engine(DATABASE_URL, echo=True,
                       future=True, poolclass=NullPool)
Base = declarative_base(bind=engine)
