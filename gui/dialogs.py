# gui/dialogs.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QDialogButtonBox
from .styles import StyleSheet


class DataRangeDialog(QDialog):
    def __init__(self, parent=None):
        """
        Initialize the DataRangeDialog with a parent widget.

        Parameters:
            parent (QWidget): The parent widget.
        """
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface for the DataRangeDialog.
        """
        self.setWindowTitle("Duplicate Data Detected")
        self.setStyleSheet(StyleSheet.DIALOG)
        layout = QVBoxLayout(self)

        message = QLabel("Duplicate data found in the uploaded file!")
        message.setStyleSheet(StyleSheet.DIALOG_LABEL)
        layout.addWidget(message)

        button_box = QDialogButtonBox()
        replace_btn = QPushButton("Complete Replacement")
        new_only_btn = QPushButton("Save Only New Data")
        cancel_btn = QPushButton("Cancel")

        for btn in [replace_btn, new_only_btn, cancel_btn]:
            btn.setStyleSheet(StyleSheet.BUTTON)
            button_box.addButton(btn, QDialogButtonBox.ActionRole)

        button_box.clicked.connect(self.handle_click)
        layout.addWidget(button_box)

    def handle_click(self, button):
        """
        Handle button clicks in the dialog.

        Parameters:
            button (QPushButton): The clicked button.
        """
        if button.text() == "Complete Replacement":
            self.parent().data_processor.set_mode("replace")
            self.accept()
        elif button.text() == "Save Only New Data":
            self.parent().data_processor.set_mode("new_only")
            self.accept()
        else:
            self.reject()
