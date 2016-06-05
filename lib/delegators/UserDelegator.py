from lib.ComboBoxDelegate import ComboBoxDelegate
from models import Users


class UserDelegator(ComboBoxDelegate):

    def __init__(self, parent=None):
        super(UserDelegator, self).__init__(parent, model_class=Users,
                                            show_field='full_name')
