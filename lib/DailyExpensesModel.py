# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5.QtSql import *
from lib.Utils import _log
from lib.CustomQueryModel import CustomQueryModel
from lib.extensions import db
from models import Items, Categories, Currencies, Locations


class DailyExpensesModel():

    def __init__(self, parent=None):
        self.db = self.db_connect()
        self.orm_db = db

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
                note, datetime)
                VALUES (:item_id, :category_id, :cost, :currency_id, :user_id,
                :place_id, :qty, :measure_id, :is_spending, :note, :datetime)
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

    def insert_item(self, name):
        try:
            new_item = Items(name=name)
            self.orm_db.add(new_item)
            self.orm_db.commit()
            return new_item.id
        except Exception as e:
            _log(e)
            return

    def get_categories(self):
        return self.orm_db.query(Categories).all()

    def get_items(self):
        return self.orm_db.query(Items).all()

    def get_currencies(self):
        return self.orm_db.query(Currencies).all()

    def get_locations(self):
        return self.orm_db.query(Locations).all()

    def get_places(self):
        places = []
        select_places_query = QSqlQuery(db=self.db)
        if not select_places_query.exec_(
            """
            SELECT p.id, p.name, l.city, l.country
            FROM places p
            LEFT JOIN locations l ON p.location_id = l.id
            ORDER BY p.id
            """
        ):
            _log("Places selection error[%s]: %s" % (
                select_places_query.lastError().type(),
                select_places_query.lastError().text()
            ))
        while select_places_query.next():
            record = select_places_query.record()
            places.append({
                'id': record.value('id'),
                'name': record.value('name'),
                'location':
                    record.value('city') + ', ' + record.value('country'),
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
