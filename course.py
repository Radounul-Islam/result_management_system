import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QGridLayout, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
import sqlite3
class CourseManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.button_clicked()
        self.load_courses()
       
       


    def initUI(self):
        self.setStyleSheet(self.get_stylesheet())  # Apply CSS

        # Layouts
        main_layout = QVBoxLayout()
        form_layout = QGridLayout()
        button_layout = QHBoxLayout()
        table_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
         # === Header ===
        header = QLabel("Manage Course Details")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Labels and Inputs
        self.lbl_course_name = QLabel("Course ID:")
        self.txt_course_id = QLineEdit()

        self.lbl_course_name = QLabel("Course Name:")
        self.txt_course_name = QLineEdit()

        self.lbl_duration = QLabel("Duration:")
        self.txt_duration = QLineEdit()

        self.lbl_charges = QLabel("Charges:")
        self.txt_charges = QLineEdit()

        self.lbl_description = QLabel("Description:")
        self.txt_description = QTextEdit()

        # Form layout
        form_layout.addWidget(self.lbl_course_name, 0, 0)
        form_layout.addWidget(self.txt_course_name, 0, 1)

        form_layout.addWidget(self.lbl_duration, 1, 0)
        form_layout.addWidget(self.txt_duration, 1, 1)

        form_layout.addWidget(self.lbl_charges, 2, 0)
        form_layout.addWidget(self.txt_charges, 2, 1)

        form_layout.addWidget(self.lbl_description, 3, 0)
        form_layout.addWidget(self.txt_description, 3, 1)

        # Buttons
        self.btn_save = QPushButton("Save")
        self.btn_update = QPushButton("Update")
        self.btn_delete = QPushButton("Delete")
        self.btn_clear = QPushButton("Clear")
        self.btn_delete.setObjectName("btn_delete")
        self.btn_update.setObjectName("btn_update")
        self.btn_clear.setObjectName("btn_clear")

        # Button layout
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_update)
        button_layout.addWidget(self.btn_delete)
        button_layout.addWidget(self.btn_clear)

        # Search
        self.lbl_search = QLabel("Course Name")
        self.txt_search = QLineEdit()
        self.btn_search = QPushButton("Search")

        search_layout.addWidget(self.lbl_search)
        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(self.btn_search)

        # Table
        
        self.table = QTableWidget()
     
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Course ID", "Name", "Duration", "Charges", "Description"])
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 70)
        self.table.setColumnWidth(4, 200)
        
       
        



        
        



        # Table layout
        table_layout.addLayout(search_layout)
        table_layout.addWidget(self.table)

        # Add layouts to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(table_layout)

        self.setLayout(main_layout)

    def button_clicked(self):
        self.btn_save.clicked.connect(self.save_course)
        self.btn_update.clicked.connect(self.update_course)
        self.btn_delete.clicked.connect(self.delete_course)
        self.btn_clear.clicked.connect(self.clear_fields)
        self.btn_search.clicked.connect(self.search_course)
       

        
    def search_course(self):
        course_name = self.txt_search.text().strip()
        if not course_name:
            QMessageBox.warning(self, "Input Error", "Please enter the course name to search.")
            return
        con = sqlite3.connect("rms.db")
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM course WHERE name=?", (course_name,))
            result = cursor.fetchone()
            if result:
                self.txt_course_name.setText(result[1])
                self.txt_duration.setText(result[2])
                self.txt_charges.setText(result[3])
                self.txt_description.setPlainText(result[4])
            else:
                QMessageBox.information(self, "No Result", "No course found with that name.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()
            self.txt_search.clear()  # Clear search field
        # Clear search field
        
    def clear_fields(self):
        self.txt_course_name.clear()
        self.txt_duration.clear()
        self.txt_charges.clear()
        self.txt_description.clear()
        self.txt_search.clear()
       # Set focus back to course name field

    def delete_course(self):
        course_name = self.txt_course_name.text()
        if not course_name:
            QMessageBox.warning(self, "Input Error", "Please enter the course name to delete.")
            return
        con = sqlite3.connect("rms.db")
        cursor = con.cursor()
        try:
            option = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete course {course_name}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if option == QMessageBox.No:
                return
            cursor.execute("DELETE FROM course WHERE name=?", (course_name,))
            con.commit()
         
            #self.clear_fields()
            self.load_courses()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()
    def update_course(self):
        course_name = self.txt_course_name.text().strip()
        duration = self.txt_duration.text().strip()
        charges = self.txt_charges.text().strip()
        description = self.txt_description.toPlainText().strip()

        if not course_name:
            QMessageBox.warning(self, "Input Error", "Please enter the course name.")
            return
        con = sqlite3.connect("rms.db")
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE course SET duration=?, charges=?, description=? WHERE name=?",
                           (duration, charges, description, course_name))
            con.commit()
            QMessageBox.information(self, "Success", "Course details updated successfully.")
            #self.clear_fields()
            self.load_courses()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()
        

    def save_course(self):

        course_name = self.txt_course_name.text().strip()
        duration = self.txt_duration.text().strip()
        charges = self.txt_charges.text().strip()
        description = self.txt_description.toPlainText().strip()

        if not course_name:
            QMessageBox.warning(self, "Input Error", "Please enter the course name.")
            return
        con = sqlite3.connect("rms.db")
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO course (name, duration, charges, description) VALUES (?, ?, ?, ?)",
                           (course_name, duration, charges, description))
            con.commit()
            QMessageBox.information(self, "Success", "Course details saved successfully.")
            #self.clear_fields()
            self.load_courses()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()
        
  
    def load_courses(self):
        con = sqlite3.connect("rms.db")
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM course")
            courses = cursor.fetchall()
            self.table.setRowCount(0)
            for row in courses:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for column, data in enumerate(row):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(Qt.ItemIsEnabled)
                    self.table.setItem(row_position, column, item)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()
        
 

    def get_stylesheet(self):
        return """
        QWidget {
            background-color: #f5f5f5;
            font-family: Arial, sans-serif;
        }
        #header {
        background-color: #002855;
        color: white;
        font-size: 22px;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
        
        QLabel {
            font-size: 14px;
            font-weight: bold;
            color: #333;
            border-radius: 5px;
            padding: 5px;
            background-color: #eaeaea;
            border: 1px solid #ccc;
        }

        QLineEdit, QTextEdit {
            background-color: #ffffff;
            border: 2px solid #ccc;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: #333;
        }
        QLineEdit:focus, QTextEdit:focus {
            border: 2px solid #0078D7;
            background-color: #f0f8ff;
        }
     

        QPushButton {
            background-color: #0078D7;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
        }

        QPushButton:hover {
            background-color: #005A9E;
        }

        QPushButton#btn_delete {
            background-color: #D9534F;
        }

        QPushButton#btn_delete:hover {
            background-color: #C9302C;
        }

        QPushButton#btn_update {
            background-color: #5CB85C;
        }

        QPushButton#btn_update:hover {
            background-color: #4CAE4C;
        }

        QPushButton#btn_clear {
            background-color: #6C757D;
        }

        QPushButton#btn_clear:hover {
            background-color: #5A6268;
        }

        QTableWidget {
            background-color: white;
            border: 2px solid #ccc;
            border-radius: 5px;
        }

        QHeaderView::section {
            background-color: #0078D7;
            color: white;
            font-size: 14px;
            padding: 5px;
        }

        QMessageBox QPushButton {
            background-color: #00aaff;
            color: white;
            padding: 6px 20px;
            font-weight: bold;
            border: 1px solid black;
            border-radius: 4px;
        }

        QMessageBox QPushButton:hover {
            background-color: #007acc;
        }
        """

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CourseManager()

    # Set unique IDs for buttons to apply different styles
  

    window.show()
    sys.exit(app.exec_())
