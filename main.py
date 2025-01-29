import sys
from PyQt5.QtWidgets import QApplication
from database.db_manager import DatabaseManager
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    db = DatabaseManager()
    window = MainWindow(db)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
