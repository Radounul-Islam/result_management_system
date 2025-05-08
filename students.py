
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, 
    QGridLayout, QFrame, QSizePolicy, QTableWidget, QTableWidgetItem, QHBoxLayout,QMessageBox

)
import sqlite3

from PyQt5.QtGui import  QCursor
from PyQt5.QtCore import Qt





class StudentDetailsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.buttons_connect()
        self.load_students()


    

    def initUI(self):
        self.setStyleSheet(self.style_sheet())
        # === Main Layout (Horizontal) ===
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

       
        # === Header ===
        header = QLabel("Manage Student Details")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # === Form Container ===
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        form_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        form_layout = QGridLayout(form_frame)

        # === Labels & Inputs ===
        self.roll_input = QLineEdit()
        self.dob_input = QLineEdit()
        self.name_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.email_input = QLineEdit()
        self.admission_input = QLineEdit()


        self.gender_combo = QComboBox()
        self.gender_combo.setCursor(QCursor(Qt.PointingHandCursor))
        self.gender_combo.addItems(["Select", "Male", "Female", "Other"])

        self.course_combo = QComboBox()
        self.course_combo.setCursor(QCursor(Qt.PointingHandCursor))
        self.courses = self.get_courses()
        self.course_combo.addItems(["All"] + self.courses)
       

        self.state_input = QLineEdit()
        self.city_input = QLineEdit()
        self.pin_input = QLineEdit()
        self.address_input = QLineEdit()

        # === Form Grid ===
        form_layout.addWidget(QLabel("Roll No."), 0, 0)
        form_layout.addWidget(self.roll_input, 0, 1)
        form_layout.addWidget(QLabel("D.O.B."), 0, 2)
        form_layout.addWidget(self.dob_input, 0, 3)

        form_layout.addWidget(QLabel("Name"), 1, 0)
        form_layout.addWidget(self.name_input, 1, 1)
        form_layout.addWidget(QLabel("Contact"), 1, 2)
        form_layout.addWidget(self.contact_input, 1, 3)

        form_layout.addWidget(QLabel("Email"), 2, 0)
        form_layout.addWidget(self.email_input, 2, 1)
        form_layout.addWidget(QLabel("Admission"), 2, 2)
        form_layout.addWidget(self.admission_input, 2, 3)

        form_layout.addWidget(QLabel("Gender"), 3, 0)
        form_layout.addWidget(self.gender_combo, 3, 1)
        form_layout.addWidget(QLabel("Course"), 3, 2)
        form_layout.addWidget(self.course_combo, 3, 3)

        form_layout.addWidget(QLabel("State"), 4, 0)
        form_layout.addWidget(self.state_input, 4, 1)
        form_layout.addWidget(QLabel("City"), 4, 2)
        form_layout.addWidget(self.city_input, 4, 3)

        form_layout.addWidget(QLabel("Pin"), 5, 0)
        form_layout.addWidget(self.pin_input, 5, 1)
        form_layout.addWidget(QLabel("Address"), 5, 2)
        form_layout.addWidget(self.address_input, 5, 3)

        main_layout.addWidget(form_frame)

        # === Buttons ===
        button_layout = QGridLayout()
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.update_btn = QPushButton("Update")
        self.update_btn.setObjectName("updateBtn")
        self.update_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("deleteBtn")
        self.delete_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setCursor(QCursor(Qt.PointingHandCursor))

        button_layout.addWidget(self.save_btn, 0, 0)
        button_layout.addWidget(self.update_btn, 0, 1)
        button_layout.addWidget(self.delete_btn, 0, 2)
        button_layout.addWidget(self.clear_btn, 0, 3)

        main_layout.addLayout(button_layout)

        # === Add Form Layout to Main Layout ===
      

        search_bar_layout = QHBoxLayout()
       
        roll_label = QLabel("Roll No.")
        roll_label.setObjectName("roll_label")
        roll_label.setAlignment(Qt.AlignLeft)

        self.roll_field = QLineEdit()
        self.search_btn = QPushButton("Search")
        self.search_btn.setObjectName("searchBtn")
        self.search_btn.setCursor(QCursor(Qt.PointingHandCursor))

        search_bar_layout.addWidget(roll_label)
        search_bar_layout.addWidget(self.roll_field)
        search_bar_layout.addWidget(self.search_btn)

        main_layout.addLayout(search_bar_layout)

        # === Footer Section ===
        self.table = QTableWidget()
        self.table.setColumnCount(12)  
        # Adjust based on your data
         # Initially no rows
        self.table.setHorizontalHeaderLabels(["Roll No.", "Name", "Email", "Gender", "D.O.B", "Contact", "Admission", "Course", "State", "City", "Pin", "Address"])
        self.table.setObjectName("tableWidget")
        
        self.table.setColumnWidth(0, 100)  # Roll No.
        self.table.setColumnWidth(1, 150)  # Name
        self.table.setColumnWidth(2, 200)  # Email

        # === Sample Data (For Testing) ===
       
        # === Add Table to Main Layout ===
        main_layout.addWidget(self.table)

    def buttons_connect(self):
        self.clear_btn.clicked.connect(self.clear_fields)
        self.save_btn.clicked.connect(self.save_student)
        self.update_btn.clicked.connect(self.update_student)
        self.delete_btn.clicked.connect(self.delete_student)
        self.search_btn.clicked.connect(self.search_student)
    

    def clear_fields(self):
        self.roll_input.clear()
        self.dob_input.clear()
        self.name_input.clear()
        self.contact_input.clear()
        self.email_input.clear()
        self.admission_input.clear()
        self.gender_combo.setCurrentIndex(0)
        self.course_combo.setCurrentIndex(0)
        self.state_input.clear()
        self.city_input.clear()
        self.pin_input.clear()
        self.address_input.clear()
        self.roll_input.setFocus()
        # for updating the course combo box
     

    def save_student(self):
        # Implement save functionality
        
        roll = self.roll_input.text().strip()
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        dob  = self.dob_input.text().strip()
        contact = self.contact_input.text().strip()
        admission = self.admission_input.text().strip()
        gender = self.gender_combo.currentText()
        course = self.course_combo.currentText()
        state = self.state_input.text().strip()
        city = self.city_input.text().strip()
        pin = self.pin_input.text().strip()
        address = self.address_input.text().strip()
        
        # Add your database save logic here
        if roll == "":
            QMessageBox.warning(self, "Input Error", "Roll No. cannot be empty.")
            return
        
     
            

        con = sqlite3.connect(database="rms.db")
        cursor = con.cursor()
        try:
            if course == "All":
                for course in self.courses: 
                    cursor.execute(
                        "INSERT INTO student(roll, name, email, gender, dob, contact, admission, course, state, city, pin, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                        (roll, name, email, gender, dob, contact, admission, course, state, city, pin, address)
                    )
                    con.commit()
            else:
                cursor.execute(
                        "INSERT INTO student(roll, name, email, gender, dob, contact, admission, course, state, city, pin, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                        (roll, name, email, gender, dob, contact, admission, course, state, city, pin, address)
                    )
                con.commit()

            QMessageBox.information(self, "Success", "Student details saved successfully.")
            self.load_students()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()


    def update_student(self):
        roll = self.roll_input.text().strip()
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        dob  = self.dob_input.text().strip()
        contact = self.contact_input.text().strip()
        admission = self.admission_input.text().strip()
        gender = self.gender_combo.currentText()
        course = self.course_combo.currentText()
        state = self.state_input.text().strip()
        city = self.city_input.text().strip()
        pin = self.pin_input.text().strip()
        address = self.address_input.text().strip()
        # Add your database save logic here
        if roll == "":
            QMessageBox.warning(self, "Input Error", "Roll No. cannot be empty.")
            return
       
        
        con = sqlite3.connect(database="rms.db")
        cursor = con.cursor()
        # Check if the student exists
        try:
            if course == "All":
                cursor.execute(
                    "UPDATE student SET roll = ?, name = ?, email = ?, gender = ?, dob = ?, contact = ?, admission = ?, state = ?, city = ?, pin = ?, address = ? WHERE roll = ?", 
                    (roll, name, email, gender, dob, contact, admission, state, city, pin, address, roll)
                )
                con.commit()   

            else:
                cursor.execute(
                    "UPDATE student SET roll = ?, name = ?, email = ?, gender = ?, dob = ?, contact = ?, admission = ?, state = ?, city = ?, pin = ?, address = ? WHERE roll = ? and course = ?", 
                    (roll, name, email, gender, dob, contact, admission, state, city, pin, address, roll, course)
                )
                con.commit()   

            QMessageBox.information(self, "Success", "Student details updated successfully.")
            self.load_students()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()
        

        
    def delete_student(self):
        roll = self.roll_input.text().strip()
        course = self.course_combo.currentText()

        # Add your database save logic here
        if roll == "":
            QMessageBox.warning(self, "Input Error", "Roll No. cannot be empty.")
            return
    
        con = sqlite3.connect(database="rms.db")
        cursor = con.cursor()
        try:
           
            if course == "All":
                option = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete student roll = {roll}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
                if option == QMessageBox.No:
                    return
                cursor.execute("DELETE FROM student WHERE roll = ?", (roll,))
            else:
                
                option = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete student roll = {roll} course = {course}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
                if option == QMessageBox.No:
                    return
                cursor.execute("DELETE FROM student WHERE roll = ? and course = ?", (roll, course))

            con.commit()

            self.load_students()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()

    # Function for search student  
    def search_student(self):
        roll = self.roll_field.text().strip()
        
        if roll == "":
            QMessageBox.warning(self, "Input Error", "Roll No. cannot be empty.")
            return
      
        con = sqlite3.connect(database="rms.db")
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM student WHERE roll = ?", (roll,))
            student = cursor.fetchone()
            if student:
               
                self.roll_input.setText(str(student[0]))
                self.name_input.setText(student[1])
                self.email_input.setText(student[2])
                self.gender_combo.setCurrentText(student[3])
                self.dob_input.setText(student[4])
                self.contact_input.setText(student[5])
                self.admission_input.setText(student[6])
                self.course_combo.setCurrentText(student[7])
                self.state_input.setText(student[8])
                self.city_input.setText(student[9])
                self.pin_input.setText(student[10])
                self.address_input.setText(student[11])
                self.roll_input.setFocus()
            else:
                QMessageBox.warning(self, "Not Found", f"No student found with roll number {roll}.")
                self.roll_field.setFocus()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()
            


    def get_courses(self):
        # Implement logic to fetch courses from the database
        # and populate the course_combo box.
        course_list = []
        con = sqlite3.connect("rms.db")
        cursor = con.cursor()
        try:
            cursor.execute("SELECT name FROM course")
            courses = cursor.fetchall()
            for course in courses:
                course_list.append(course[0])
            
        
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            con.close()

        return course_list


   

    def load_students(self):
        con = sqlite3.connect("rms.db")
        cursor = con.cursor()
        try:
            cursor.execute("SELECT  * FROM student")
            students = cursor.fetchall()
            self.table.setRowCount(0)
            for row in students:
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

 

    def style_sheet(self):
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
        
    }

    QLabel {
        font-size: 14px;
        font-weight: bold;
        border-radius: 5px;
        padding: 5px;
        color: #333;
    }
    QLabel#roll_label {
        background-color: #ccc;
        color: #000;
    }

    QLineEdit, QComboBox{
        background-color: #ffffff;
        border: 1px solid #cccccc;
        padding: 5px;
        border-radius: 3px;
        color: #333;
    }
    QLineEdit:focus{
        border: 2px solid #007bff;
        background-color: #f0f8ff;
    }
    QComboBox::drop-down {
        border: 1px solid #cccccc;
        border-radius: 3px;
    }
    QComboBox::item {
        background-color: #ffffff;
        color: #333;
    }
   


    QPushButton {
        padding: 5px;
        border-radius: 3px;
        color: white;
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

 
    QPushButton#saveBtn {
        background-color: #007bff;
       
    }
    #saveBtn:hover {
        background-color: #0056b3;
    }

    #updateBtn {
        background-color: #28a745;
      
    }
    #updateBtn:hover {
        background-color: #218838;
    }

    #deleteBtn {
        background-color: #dc3545;
        
    }
    #deleteBtn:hover {
        background-color: #c82333;
    }

    #clearBtn {
        background-color: #6c757d;

    }
    #clearBtn:hover {
        background-color: #5a6268;
    }
    #searchBtn {
        background-color: #17a2b8;

    }
    #searchBtn:hover {
        background-color: #138496;
    }

    #formFrame {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        border: 2px solid #ddd;
    
    }

    #tableWidget {
        background-color: white;
        border: 1px solid #cccccc;
 
    }
    QHeaderView::section {
        background-color: #007bff;
        color: white;
        font-size: 14px;
        padding: 5px;
    }
  
    QTableWidget::item {
        padding: 5px;
        color: #333;
        }
    
     """
    # Function to fetch courses from the database
    

    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    student_management_ui = StudentDetailsUI()
    student_management_ui.show()
    sys.exit(app.exec_())
