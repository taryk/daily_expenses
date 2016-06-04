from lib.ComboBoxDelegate import ComboBoxDelegate
from models import Items


class ItemDelegator(ComboBoxDelegate):

    def __init__(self, parent=None, db_model=None):
        super(ItemDelegator, self).__init__(parent, db_model=db_model,
                                            db_class=Items,
                                            show_field='name')
