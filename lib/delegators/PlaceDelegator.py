from lib.ComboBoxDelegate import ComboBoxDelegate
from models import Places


class PlaceDelegator(ComboBoxDelegate):

    def __init__(self, parent=None):
        super(PlaceDelegator, self).__init__(parent, model_class=Places,
                                             show_field='name')
