from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget,
    QVBoxLayout, QHBoxLayout, QHeaderView, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
import sys
import sqlite3


class StudentReportUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Result Management System")

        self.initUI()
        self.buttons_connect()

    def load_styles(self):
        return """
           QWidget {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
    }
    
        QLabel#HeaderLabel {
            background-color: orange;
            color: #4b2e00;
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            height: 50px;
            min-height: 50px;
            max-height: 50px;
            border-radius: 5px;
        }

        QLabel {
            font-size: 20px;
            font-weight: bold;
            color: #333;
            padding: 5px;
            margin: 5px;
            background-color: #e0e0e0;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-family: Arial, sans-serif;
        }

        QLineEdit {
            background-color: #ffffe0;
            padding: 5px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
            color: #333;
        }

         QLineEdit:focus{
        border: 2px solid #007bff;
        background-color: #f0f8ff;
        }
    
   
        QPushButton {
            background-color: #00aaff;
            color: white;
            padding: 6px 20px;
            font-weight: bold;
            border: 1px solid black;
            border-radius: 4px;
        }

        QPushButton:hover {
            background-color: #007acc;
        }

        QPushButton#ClearButton {
            background-color: #888888;
        }

        QPushButton#ClearButton:hover {
            background-color: #555555;
        }

        QPushButton#DeleteButton {
            background-color: red;
            padding: 8px 25px;
        }

        QPushButton#DeleteButton:hover {
            background-color: darkred;
        }

        QHeaderView::section {
            font-weight: bold;
            background-color: #0078D7;
            color: white;
            padding: 4px;
            border: 1px solid lightgray;
           
        }
    
        QTableWidget::item {
            padding: 5px;
            border-bottom: 1px solid #ccc;
            color: #333;
        }
        
    
        """

    def initUI(self):
        self.setStyleSheet(self.load_styles())
        main_layout = QVBoxLayout()

        main_layout.setSpacing(10)

        # Header
        header = QLabel("View Student Results")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("HeaderLabel")
        main_layout.addWidget(header)

        # Search Section
        search_layout = QHBoxLayout()
        search_label = QLabel("Search By Roll No.")
        self.search_input = QLineEdit()
        self.search_input.setFixedWidth(150)

        self.search_button = QPushButton("Search")
        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("ClearButton")
        self.search_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.clear_button.setCursor(QCursor(Qt.PointingHandCursor))
        

        search_layout.addStretch()
        search_layout.addWidget(search_label)
        search_layout.addSpacing(10)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.clear_button)
        search_layout.addStretch()

        main_layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Roll No", "Name", "Course", "Marks Obtained", "Total Marks", "Percentage"
        ])
        #self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 250)
        self.table.setColumnWidth(3,150)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 150)
        self.table.setObjectName("ResultTable")
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
      
   
        self.table.setFixedHeight(200)
        main_layout.addWidget(self.table)

        # Delete Button
        self.delete_button = QPushButton("Delete")
        self.delete_button.setObjectName("DeleteButton")
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))

        delete_layout = QHBoxLayout()
        delete_layout.addStretch()
        delete_layout.addWidget(self.delete_button)
        delete_layout.addStretch()

        main_layout.addLayout(delete_layout)
        self.setLayout(main_layout)

    def buttons_connect(self):
        self.search_button.clicked.connect(self.search_student)
        self.clear_button.clicked.connect(self.clear_search)
        self.delete_button.clicked.connect(self.delete_student)

    def search_student(self):
        con = sqlite3.connect(database="rms.db")
        cursor = con.cursor()
        try:
            roll_no = self.search_input.text().strip()
            if not roll_no:
                QMessageBox.warning(self, "Input Error", "Please enter a roll number.")
                return
            cursor.execute("SELECT * FROM result WHERE roll =?", (roll_no,))
            result = cursor.fetchone()
            if result:
                self.table.clearContents()
                self.table.setRowCount(0)
                self.table.setRowCount(1)
                for i, value in enumerate(result):
                    if i !=  0:
                        item = QTableWidgetItem(str(value))
                        item.setFlags(Qt.ItemIsEnabled)
                        self.table.setItem(0, i - 1, item)
                        
            else:
                QMessageBox.warning(self, "Not Found", f"No student found with this roll number .")
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()
            self.search_input.clear()

    def clear_search(self):
        self.search_input.clear()
        self.search_input.setFocus()

    def delete_student(self):
        con = sqlite3.connect(database="rms.db")
        cursor = con.cursor()
        try:
            
            if self.table.rowCount() == 0:
                QMessageBox.warning(self, "Selection Error", "No student selected.")
                return
            selected_row = 0
            roll_no = self.table.item(selected_row, 0).text().strip()

            # for confirmation message
            option = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete the result for roll number {roll_no}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if option == QMessageBox.No:
                return
            # Delete the student result from the database
            cursor.execute("DELETE FROM result WHERE roll=?", (roll_no,))
            con.commit()
            self.table.setRowCount(0)
            self.table.clearContents()
            self.search_input.clear()
            self.search_input.setFocus()

            # Show success message
            QMessageBox.information(self, "Success", "Student result deleted successfully.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentReportUI()
    window.show()
    sys.exit(app.exec_())
