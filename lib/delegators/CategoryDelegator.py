from lib.ComboBoxDelegate import ComboBoxDelegate
from models import Categories


class CategoryDelegator(ComboBoxDelegate):

    def __init__(self, parent=None, db_model=None):
        super(CategoryDelegator, self).__init__(parent, db_model=db_model,
                                                db_class=Categories,
                                                show_field='name')
