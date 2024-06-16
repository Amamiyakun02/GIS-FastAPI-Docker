from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy.ext.declarative import declarative_base
load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(autocommit=False, bind=engine, autoflush=True)


Base = declarative_base()


