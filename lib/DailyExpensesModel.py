# -*- coding: utf-8 -*-

from lib.CustomQueryModel import CustomQueryModel
from lib.extensions import db


class DailyExpensesModel():

    def __init__(self, parent=None):
        self.db = db

    def get_table_view_model(self):
        return CustomQueryModel(db=self.db).get_model()
