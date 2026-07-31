from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCEHEMY_URL = "sqlite:///./todosapp.db"

engine = create_engine(SQLALCEHEMY_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False,autocommit=False, bind=engine)

Base = declarative_base()