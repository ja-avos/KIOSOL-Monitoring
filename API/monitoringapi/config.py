from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import models
import os

DATABASE_HOST = os.getenv('POSTGRES_HOST', '157.253.242.151')
DATABASE_USERNAME = os.getenv('POSTGRES_USER', 'labmonitoring')
DATABASE_PASSWD = os.getenv('POSTGRES_PASSWORD', 'IOT2022!')
DATABASE_NAME = os.getenv('POSTGRES_DB', 'solarlabmonitoring')
DATABASE_PORT = os.getenv('POSTGRES_PORT', '5432')

DATABASE_URL = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)