import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


class DataBase:

    def __new__(cls):
        # Use in-memory database when testing stuff.
        db_file = '/db/daily_expenses.db' \
            if not hasattr(sys, '_called_from_test') else ''
        cls.engine = create_engine('sqlite://' + db_file, echo=True)
        Session = sessionmaker(bind=cls.engine)
        db = Session()
        Base.__class__.db = db
        return db

    @classmethod
    def create_tables(cls):
        """Creates new DB tables if they don't exist.
        """
        Base.metadata.create_all(cls.engine)
