from sqlalchemy import Column, Integer, String, DateTime, func
from models import Base


class Users(Base):
    __singular__ = 'user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    datetime_created = Column(DateTime, default=func.current_timestamp(),
                              nullable=False)
    datetime_modified = Column(DateTime, onupdate=func.current_timestamp(),
                               nullable=True)

    def title(self):
        return self.full_name

    def __repr__(self):
        return "<Users(user_name='{:s}', full_name='{:s}', " \
               "datetime_created='{:s}')>" \
            .format(self.user_name, self.full_name, self.datetime_created)
