from sqlalchemy import Column, Integer, String, Text, DateTime, func
from lib.extensions import Base


class Categories(Base):

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    datetime_created = Column(DateTime, default=func.current_timestamp(),
                              nullable=False)
    datetime_modified = Column(DateTime, onupdate=func.current_timestamp(),
                               nullable=True)

    def __repr__(self):
        return "<Categories(name='{:s}', description='{:s}', " \
               "datetime_created='{:s}')>" \
            .format(self.name, self.description, self.datetime_created)
