from lib.ComboBoxDelegate import ComboBoxDelegate
from models import Users


class UserDelegator(ComboBoxDelegate):

    def __init__(self, parent=None, db_model=None):
        super(UserDelegator, self).__init__(parent, db_model=db_model,
                                            db_class=Users,
                                            show_field='full_name')
