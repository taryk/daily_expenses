from lib.ComboBoxDelegate import ComboBoxDelegate
from models import Categories


class CategoryDelegator(ComboBoxDelegate):

    def __init__(self, parent=None):
        super(CategoryDelegator, self).__init__(parent, model_class=Categories,
                                                show_field='name')
