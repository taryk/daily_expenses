from sqlalchemy import Column, Integer, String, Text, DateTime, func
from dailyexpenses.extensions import Base


class Categories(Base):
    __singular__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    datetime_created = Column(DateTime, default=func.current_timestamp(),
                              nullable=False)
    datetime_modified = Column(DateTime, onupdate=func.current_timestamp(),
                               nullable=True)

    def title(self):
        return self.name

    def __repr__(self):
        return "<Categories(name='{:s}', description='{:s}', " \
               "datetime_created='{:s}')>" \
            .format(self.name, self.description, self.datetime_created)
