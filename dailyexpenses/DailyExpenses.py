from PyQt5.QtWidgets import QApplication
from dailyexpenses.MainWindow import MainWindow


class DailyExpenses:

    def __init__(self, argv):
        self.app = QApplication(argv)
        self.main_window = None

    def run(self):
        self.main_window = MainWindow()
        self.main_window.show()
        return self.app.exec_()
