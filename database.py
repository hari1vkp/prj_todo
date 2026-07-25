import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv

load_dotenv()
db_url=os.getenv("db_url")
engine=create_engine(db_url)
sessionlocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)
base=declarative_base()

