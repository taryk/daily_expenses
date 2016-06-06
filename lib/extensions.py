from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///db/daily_expenses.db', echo=True)

Base = declarative_base(cls=Base)

Session = sessionmaker(bind=engine)
db = Session()
Base.__class__.db = db

def init_db():
    # import models
    # Base.metadata.create_all(engine)
    print("init db")
