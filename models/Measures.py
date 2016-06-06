from sqlalchemy import Column, Integer, String, Text, DateTime, func
from lib.extensions import Base


class Measures(Base):
    __singular__ = 'measure'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    short = Column(String(10), unique=True, nullable=False)
    note = Column(Text, nullable=True)
    datetime_created = Column(DateTime, default=func.current_timestamp(),
                              nullable=False)
    datetime_modified = Column(DateTime, onupdate=func.current_timestamp(),
                               nullable=True)

    def title(self):
        return '{:s} ({:s})'.format(self.name, self.short)

    def __repr__(self):
        return "<Measures(name='{:s}', short='{:s}', " \
               "datetime_created='{:s}')>"\
            .format(self.name, self.short, self.datetime_created)
