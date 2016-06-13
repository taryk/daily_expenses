from PyQt5.QtWidgets import QApplication
from dailyexpenses.extensions import DataBase
from dailyexpenses.MainWindow import MainWindow


class DailyExpenses:

    def __init__(self, argv):
        self.app = QApplication(argv)
        self.main_window = None
        self.db = DataBase()

    def run(self):
        # Create all tables if they don't exist yet.
        DataBase.create_tables()
        self.main_window = MainWindow()
        self.main_window.show()
        return self.app.exec_()
