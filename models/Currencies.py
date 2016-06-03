from sqlalchemy import Column, Integer, String, DateTime, func
from lib.extensions import Base


class Currencies(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    name = Column(String(3), unique=True, nullable=False)
    sign = Column(String(2), nullable=False)
    note = Column(String(100), nullable=True)
    datetime_created = Column(DateTime, default=func.current_timestamp(),
                              nullable=False)
    datetime_modified = Column(DateTime, onupdate=func.current_timestamp(),
                               nullable=True)

    def __repr__(self):
        return "<Currencies(name='{:s}', sign='{:s}', datetime_created='{" \
               ":s}')>".format(self.name, self.sign, self.datetime_created)