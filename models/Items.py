from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import validates
from lib.extensions import Base


class Items(Base):
    __singular__ = 'item'

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
        return "<Items(name='{:s}', description='{:s}', " \
               "datetime_created='{:s}')>" \
            .format(self.name, self.description, self.datetime_created)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise Exception("Item's name can't be empty.")
        return name

    @classmethod
    def insert(cls, name):
        new_item = Items(name=name)
        cls.db.add(new_item)
        cls.db.commit()
        return new_item.id
