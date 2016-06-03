from sqlalchemy import ForeignKey, Column, Integer, String, Text, DateTime, \
    UniqueConstraint, func
from sqlalchemy.orm import relationship
from lib.extensions import Base


class Places(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    location = relationship("Locations")
    note = Column(Text, nullable=True)
    datetime_created = Column(DateTime, default=func.current_timestamp(),
                              nullable=False)
    datetime_modified = Column(DateTime, onupdate=func.current_timestamp(),
                               nullable=True)

    __table_args__ = (
        UniqueConstraint('name', 'location_id', name='name_location_id_uc'),
    )

    def __repr__(self):
        return "<Places(name='{:s}', location_name='{:s}', " \
               "datetime_created='{:s}')>" \
            .format(self.name, self.location.name, self.datetime_created)