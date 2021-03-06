from sqlalchemy import Column, Integer, String, Text, DateTime, \
    UniqueConstraint, func
from models import Base


class Locations(Base):
    __singular__ = 'location'

    id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    note = Column(Text, nullable=True)
    datetime_created = Column(DateTime, default=func.current_timestamp(),
                              nullable=False)
    datetime_modified = Column(DateTime, onupdate=func.current_timestamp(),
                               nullable=True)

    __table_args__ = (
        UniqueConstraint('city', 'country', name='city_country_uc'),
    )

    def title(self):
        return self.city + ' ' + self.country

    def __repr__(self):
        return "<Locations(city='{:s}', country='{:s}', " \
               "datetime_created='{:s}')>" \
            .format(self.city, self.country, self.datetime_created)
