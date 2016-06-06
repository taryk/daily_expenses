from sqlalchemy.ext.declarative import declared_attr


class Base(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = None

    __singular__ = None
    __depend_on__ = ()
    __extra_data__ = ('id',)

    def __repr__(self):
        return "<{:s}(id={:d})>".format(self.__class__.__str__(), self.id)

    def title(self):
        pass

    def extra_data(self):
        return dict(
            zip(
                self.__extra_data__,
                map(lambda field: getattr(self, field), self.__extra_data__)
            )
        )

    @classmethod
    def all(cls):
        return cls.db.query(cls).all()
