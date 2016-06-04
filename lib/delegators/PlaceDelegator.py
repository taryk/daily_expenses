from lib.ComboBoxDelegate import ComboBoxDelegate
from models import Places


class PlaceDelegator(ComboBoxDelegate):

    def __init__(self, parent=None, db_model=None):
        super(PlaceDelegator, self).__init__(parent, db_model=db_model,
                                             db_class=Places,
                                             show_field='name')
