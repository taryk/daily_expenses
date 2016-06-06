from sqlalchemy.ext.declarative import declared_attr


class Base(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        return "<{:s}(id={:d})>".format(self.__class__.__str__(), self.id)

    @classmethod
    def all(cls):
        return cls.db.query(cls).all()
