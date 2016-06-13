from dailyexpenses.ComboBoxDelegate import ComboBoxDelegate
from models import Items


class ItemDelegator(ComboBoxDelegate):

    def __init__(self, parent=None):
        super(ItemDelegator, self).__init__(parent, model_class=Items,
                                            show_field='name')
