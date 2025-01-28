import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from database.db_manager import DatabaseManager

def main():
    app = QApplication(sys.argv)
    db = DatabaseManager()
    window = MainWindow(db)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
