from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlalchemy_database_url = 'postgresql://postgres:password123@localhost/fastapi'

engine = create_engine(sqlalchemy_database_url)
