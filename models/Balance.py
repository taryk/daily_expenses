from sqlalchemy import ForeignKey, Column, Integer, Float, SmallInteger, \
    Text, DateTime, func
from sqlalchemy.orm import relationship
from lib.extensions import Base


class Balance(Base):
    __tablename__ = 'balance'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    item = relationship("Items")
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship("Categories")
    cost = Column(Float, nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)
    currency = relationship("Currencies")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("Users")
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    place = relationship("Places")
    qty = Column(Float, nullable=False)
    measure_id = Column(Integer, ForeignKey('measures.id'), nullable=False)
    measure = relationship("Measures")
    is_spending = Column(SmallInteger, nullable=False)
    note = Column(Text, nullable=True)
    datetime = Column(DateTime, default=func.current_timestamp(),
                      nullable=False)
    datetime_created = Column(DateTime, default=func.current_timestamp(),
                              nullable=False)
    datetime_modified = Column(DateTime, onupdate=func.current_timestamp(),
                               nullable=True)

    def __repr__(self):
        return "<Balance(item_name='{:s}', cost='{:s}', currency='{:s}' " \
               "datetime='{:s}')>" \
            .format(self.item.name, self.cost, self.currency.name,
                    self.datetime_created)
