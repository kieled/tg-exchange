from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = 'yourDB'
# DATABASE_URL = 'sqlite:///./db.sqlite'
Base = declarative_base()

engine = create_engine(DATABASE_URL)

session = sessionmaker(
    engine, autoflush=False, autocommit=False
)