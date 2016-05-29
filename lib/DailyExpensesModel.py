# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5.QtSql import *
from lib.Utils import _log
from lib.CustomQueryModel import CustomQueryModel


class DailyExpensesModel():

    def __init__(self, parent=None):
        self.db = self.db_connect()

    def db_connect(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("db/daily_expenses.db")
        if not db.open():
            _log("Database opening error[%s]: %s" % (
                db.lastError().type(),
                db.lastError().text()
            ))
            QtGui.QMessageBox.critical(
                None, QtGui.qApp.tr("Cannot open database"),
                QtGui.qApp.tr("Unable to establish a database connection.\n\n"
                              "Click Cancel to exit."),
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton
            )
            return None
        return db

    def get_model(self):
        return CustomQueryModel(db=self.db).get_model()

    def insert(self, data=dict()):
        query_insert = QSqlQuery()
        try:
            query_insert.prepare(
                """
                INSERT INTO balance (item_id, category_id, cost,
                currency_id, user_id, place_id, qty, measure_id, is_spending,
                note, date)
                VALUES (:item_id, :category_id, :cost, :currency_id, :user_id,
                :place_id, :qty, :measure_id, :is_spending, :note, :date)
                """)
            for column in data:
                query_insert.bindValue(':'+column, data[column])

            if not query_insert.exec_():
                _log("Can't add. Error[%s]: %s" % (
                    query_insert.lastError().type(),
                    query_insert.lastError().text()
                ))
                _log("bound values: %s" % str(query_insert.boundValues()))
        except Exception as e:
            _log(e)
            return
        self.db.commit()

    def get_item_id(self, name=None):
        select_item_query = QSqlQuery(db=self.db)
        select_item_query.prepare(
            'SELECT id FROM items WHERE name = :name LIMIT 1'
        )
        select_item_query.bindValue(':name', name)
        if not select_item_query.exec_():
            _log("Can't select item. Error[%s]: %s" % (
                select_item_query.lastError().type(),
                select_item_query.lastError().text()
            ))
            _log("bound values: %s" % str(select_item_query.boundValues()))
            return None
        if select_item_query.first():
            item_id = select_item_query.record().value('id')
            return item_id
        return None

    def insert_item(self, name=None):
        insert_item_query = QSqlQuery(db=self.db)
        insert_item_query.prepare('INSERT INTO items (name) VALUES (:name)')
        insert_item_query.bindValue(':name', name)
        if not insert_item_query.exec_():
            _log("Can't add item. Error[%s]: %s" % (
                insert_item_query.lastError().type(),
                insert_item_query.lastError().text()
            ))
            _log("bound values: %s" % str(insert_item_query.boundValues()))
            return None
        self.db.commit()

    # TODO follow DRY
    def get_currencies(self):
        currencies = []
        select_currencies_query = QSqlQuery(db=self.db)
        if not select_currencies_query.exec_(
                "SELECT id, name, sign FROM currencies ORDER BY id"):
            _log("Currencies selection error[%s]: %s" % (
                select_currencies_query.lastError().type(),
                select_currencies_query.lastError().text()
            ))
            return
        while select_currencies_query.next():
            record = select_currencies_query.record()
            currencies.append({
                'id': record.value('id'),
                'name': record.value('name'),
                'sign': record.value('sign'),
            })
        return currencies

    def get_categories(self):
        categories = []
        select_categories_query = QSqlQuery(db=self.db)
        if not select_categories_query.exec_(
                'SELECT id, name FROM categories ORDER BY id'):
            _log("Categories selection error[%s]: %s" % (
                select_categories_query.lastError().type(),
                select_categories_query.lastError().text()
            ))
            return
        while select_categories_query.next():
            record = select_categories_query.record()
            categories.append({
                'id': record.value('id'),
                'name': record.value('name')
            })
        return categories

    def get_items(self):
        items = []
        select_items_query = QSqlQuery(db=self.db)
        if not select_items_query.exec_(
                'SELECT id, name FROM items ORDER BY id'):
            _log("Items selection error[%s]: %s" % (
                select_items_query.lastError().type(),
                select_items_query.lastError().text()
            ))
            return
        while select_items_query.next():
            record = select_items_query.record()
            items.append({
                'id': record.value('id'),
                'name': record.value('name'),
            })
        return items

    def get_places(self):
        places = []
        select_places_query = QSqlQuery(db=self.db)
        if not select_places_query.exec_(
                'SELECT id, name, location FROM places ORDER BY id'):
            _log("Places selection error[%s]: %s" % (
                select_places_query.lastError().type(),
                select_places_query.lastError().text()
            ))
        while select_places_query.next():
            record = select_places_query.record()
            places.append({
                'id': record.value('id'),
                'name': record.value('name'),
                'location': record.value('location'),
            })
        return places

    def get_users(self):
        users = []
        select_users_query = QSqlQuery(db=self.db)
        if not select_users_query.exec_(
                'SELECT id, user_name, full_name FROM users ORDER BY id'):
            _log("Users selection error[%s]: %s" % (
                select_users_query.lastError().type(),
                select_users_query.lastError().text()
            ))
        while select_users_query.next():
            record = select_users_query.record()
            users.append({
                'id': record.value('id'),
                'user_name': record.value('user_name'),
                'full_name': record.value('full_name'),
            })
        return users

    def get_measures(self):
        measures = []
        select_measures_query = QSqlQuery(db=self.db)
        if not select_measures_query.exec_(
                'SELECT id, name, short FROM measures ORDER BY id'):
            _log("Measures selection error[%s]: %s" % (
                select_measures_query.lastError().type(),
                select_measures_query.lastError().text()
            ))
        while select_measures_query.next():
            record = select_measures_query.record()
            measures.append({
                'id': record.value('id'),
                'name': record.value('name'),
                'short': record.value('short'),
            })
        return measures
