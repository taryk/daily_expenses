import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base

# Use in-memory database when testing stuff.
DB_FILE = '/db/daily_expenses.db' \
    if not hasattr(sys, '_called_from_test') else ''

engine = create_engine('sqlite://' + DB_FILE, echo=True)

Base = declarative_base(cls=Base)

Session = sessionmaker(bind=engine)
db = Session()
Base.__class__.db = db


def init_db():
    """Creates new DB tables if called from tests.
    """
    if hasattr(sys, '_called_from_test'):
        Base.metadata.create_all(engine)
