from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL (relative path)
db_url = 'sqlite:///mydatabase.db'

# Create the SQLAlchemy engine
engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

