from PyQt5.QtWidgets import QApplication, QComboBox, QWidget, QVBoxLayout, QLineEdit
import sys

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.combo = QComboBox()
        self.combo.setEditable(True)  # Make it editable

        # Initial items
        self.combo.addItems(["One", "Two", "Three"])

        layout = QVBoxLayout()
        layout.addWidget(self.combo)
        self.setLayout(layout)

        # Hook into the line edit (editable field)
        self.line_edit = self.combo.lineEdit()
        self.line_edit.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.line_edit and event.type() == event.FocusIn:
            self.update_combo_items()
        return super().eventFilter(obj, event)

    def update_combo_items(self):
        # Clear and update items
        self.combo.clear()
        new_items = ["Updated A", "Updated B", "Updated C"]
        self.combo.addItems(new_items)

        # Update the editable text so the change is visible
        self.combo.setCurrentIndex(0)                      # selects the first item
        self.combo.lineEdit().setText(new_items[0])        # updates the text in the field

app = QApplication(sys.argv)
window = MyWidget()
window.show()
sys.exit(app.exec_())
