import sys
import sqlite3


from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QComboBox, QScrollArea, QFrame, QSizePolicy, 
    QMessageBox
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt



class StudentResultPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.buttons_connect()

    def init_ui(self):
        self.setStyleSheet(self.get_stylesheet())

        # Main Layout (StackedWidget Compatible)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Title Label
        self.lbl_title = QLabel("Manage Course Details")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setObjectName("titleLabel")
        main_layout.addWidget(self.lbl_title)

        # FORM FRAME (This will have a visible border)
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
         # Stretch horizontally
        form_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_frame.setMinimumWidth(400) 

        form_layout = QGridLayout()
        form_layout.setSpacing(10)
        form_frame.setLayout(form_layout)
     
        # Select Student combo box
        
        self.lbl_select_student = QLabel("Select Student")
        self.cmb_student = QComboBox()
        self.cmb_student.setCursor(QCursor(Qt.PointingHandCursor))
        self.cmb_student.setObjectName("studentComboBox")
        self.cmb_student.addItems(self.get_stuent_rolls())
        self.cmb_student.setEditable(True)  # Make it editable


       
        

         # Placeholder search button
        self.btn_search = QPushButton("Search")
        self.btn_search.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_search.setObjectName("searchButton")

        # Student Name
        self.lbl_name = QLabel("Name")
        self.txt_name = QLineEdit()
        self.txt_name.setReadOnly(True)  # Make it read-only

        # Course Name
        self.lbl_course = QLabel("Select Course")
        self.txt_course = QComboBox()
        self.txt_course.setCursor(QCursor(Qt.PointingHandCursor))
        self.txt_course.setObjectName("CourseCombo")
        self.txt_course.addItems(self.get_all_courses())
 
       
        # Marks Obtained
        self.lbl_marks_obtained = QLabel("Marks Obtained")
        self.txt_marks_obtained = QLineEdit()

        # Full Marks
        self.lbl_full_marks = QLabel("Full Marks")
        self.txt_full_marks = QLineEdit()

        # Submit , Clear & Update Buttons
        self.btn_update = QPushButton("Update")
        self.btn_update.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_update.setObjectName("updateButton")
        self.btn_submit = QPushButton("Submit")
        self.btn_submit.setObjectName("submitButton")
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setObjectName("clearButton")
        self.btn_update.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_clear.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_submit.setCursor(QCursor(Qt.PointingHandCursor))

        # Image (Auto Resize for Stack Widget)
        self.lbl_image = QLabel()
        self.image_path = "images/result.jpg"  # Change image path here
        pixmap = QPixmap(self.image_path)
        self.lbl_image.setPixmap(pixmap)
          
        self.lbl_image.setMaximumSize(300, 250)
        self.lbl_image.setScaledContents(True)
        self.lbl_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lbl_image.setObjectName("imageLabel")
       
        self.lbl_image.setAlignment(Qt.AlignCenter)
        self.lbl_image.setContentsMargins(10, 10, 10, 10)

        self.lbl_image.setAlignment(Qt.AlignCenter)

        # Form Layout Setup
        form_layout.addWidget(self.lbl_select_student, 0, 0)
        form_layout.addWidget(self.cmb_student, 0, 1)
        form_layout.addWidget(self.btn_search, 0, 2)

        form_layout.addWidget(self.lbl_name, 1, 0)
        form_layout.addWidget(self.txt_name, 1, 1, 1, 2)

        form_layout.addWidget(self.lbl_course, 2, 0)
        form_layout.addWidget(self.txt_course, 2, 1, 1, 2)

        form_layout.addWidget(self.lbl_marks_obtained, 3, 0)
        form_layout.addWidget(self.txt_marks_obtained, 3, 1, 1, 2)

        form_layout.addWidget(self.lbl_full_marks, 4, 0)
        form_layout.addWidget(self.txt_full_marks, 4, 1, 1, 2)

        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_submit)
        button_layout.addWidget(self.btn_clear)
        button_layout.addWidget(self.btn_update)

        # Content Layout
        content_layout = QHBoxLayout()
        content_layout.addWidget(form_frame)  # Add Form Frame Here
        content_layout.addWidget(self.lbl_image)

        # Scrollable Container (Prevents UI issues in QStackedWidget)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_container = QWidget()
        scroll_container.setLayout(content_layout)
        scroll_area.setWidget(scroll_container)

        # Arrange Layouts
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(button_layout)



    
    def buttons_connect(self):
        self.btn_search.clicked.connect(self.load_student_details)
        self.btn_clear.clicked.connect(self.clear_fields)
        self.btn_submit.clicked.connect(self.submit_result)
        self.btn_update.clicked.connect(self.update_result)


    def get_stuent_rolls(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        students = []
        try:
            cur.execute("SELECT DISTINCT roll FROM student")
            rows = cur.fetchall()
            for row in rows:
                students.append(row[0])
        except sqlite3.Error as e:
            print(f"Error fetching student rolls: {e}")
        finally:
            con.close()

        return students
            
   
    def get_all_courses(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        courses = []
        try:
            cur.execute(f"SELECT name FROM course")
            rows = cur.fetchall()
            for row in rows:
                courses.append(row[0])
        except sqlite3.Error as e:
            print(f"Error fetching student course: {e}")
        finally:
            con.close()
        
        return courses


    def update_result(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            roll_no = self.cmb_student.currentText().strip()
            name = self.txt_name.text().strip()
            course = self.txt_course.currentText().strip()
            marks_obtained = self.txt_marks_obtained.text().strip()
            full_marks = self.txt_full_marks.text().strip()

            if not roll_no or not name or not course or not marks_obtained or not full_marks:
                QMessageBox.warning(self, "Input Error", "Please fill all fields.")
                return

            # Update result table   
            try:
                percentage = (int(marks_obtained) / int(full_marks)) * 100
            except ZeroDivisionError:
                QMessageBox.warning(self, "Input Error", "Full marks cannot be zero.")
                return
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Please enter valid numbers for marks.")
                return
            percentage = round(percentage, 2)  # Round to 2 decimal places
            percentage = str(percentage) + "%"
            cur.execute("UPDATE result SET name=?, marks_ob=?, full_marks=?, per=? WHERE roll=? and course = ?",
                        (name, marks_obtained, full_marks, percentage, roll_no, course))
            con.commit()
            if cur.rowcount == 0:
                QMessageBox.warning(self, "Not Found", "No result found for this roll number.")
                return
            # Clear fields after update
            self.txt_name.clear()
            
            QMessageBox.information(self, "Success", "Result updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating result: {e}")
        finally:
            con.close()
       
    def load_student_details(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            roll_no = self.cmb_student.currentText().strip()
            course = self.txt_course.currentText().strip()
            if not roll_no:
                self.txt_name.clear()
    
                return
            cur.execute("SELECT name, course FROM student WHERE roll=? and course=?", (roll_no, course))
            student_data = cur.fetchone()
            if student_data:
                self.txt_name.setText(student_data[0])
               
            else:
                QMessageBox.warning(self, "Not Found", f"No student found with this roll number and course {course}")
                # Clear fields if no student found
                self.txt_name.clear()

        except sqlite3.Error as e:
            print(f"Error loading student details: {e}")
        finally:
            con.close()
        

    def clear_fields(self):
        self.cmb_student.setCurrentIndex(0)
        self.txt_name.clear()
        self.txt_marks_obtained.clear()
        self.txt_full_marks.clear()
        self.txt_course.setCurrentIndex(0)

    def submit_result(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            roll_no = self.cmb_student.currentText().strip()
            name = self.txt_name.text().strip()
            course = self.txt_course.currentText().strip()
            marks_obtained = self.txt_marks_obtained.text().strip()
            full_marks = self.txt_full_marks.text().strip()

            if not roll_no or not name or not course or not marks_obtained or not full_marks:
                QMessageBox.warning(self, "Input Error", "Please fill all fields.")
                return
        
            # Insert into result table
            try:
                percentage = (int(marks_obtained) / int(full_marks)) * 100
            except ZeroDivisionError:
                QMessageBox.warning(self, "Input Error", "Full marks cannot be zero.")
                return
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Please enter valid numbers for marks.")
                return
            percentage = round(percentage, 2)  # Round to 2 decimal places
            percentage = str(percentage) + "%"
            cur.execute("INSERT INTO result (roll, name, course, marks_ob, full_marks, per) VALUES (?, ?, ?, ?, ?, ?)",
                        (roll_no, name, course, marks_obtained, full_marks, percentage))
            con.commit()
            QMessageBox.information(self, "Success", "Result submitted successfully.")
            self.txt_name.clear()
            self.txt_course.setCurrentIndex(0)
            self.cmb_student.setFocus()

        except sqlite3.Error as e:
           QMessageBox.warning(self, "Database Error!", f"{e}")
        finally:
            con.close()
        

    def get_stylesheet(self):
        return """
        QWidget {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
    }

        #titleLabel {
            font-size: 18px;
            font-weight: bold;
            background-color: #FFA500;
            color: white;
            padding: 10px;
            border-radius: 5px;
        
        }

        QLabel {
            font-size: 14px;
            font-weight: bold;
            color: #333;
            border-radius: 5px;
            background-color: #eee;
            padding: 5px;
        }


        QLineEdit, QComboBox{
        background-color: #ffffff;
        border: 1px solid #ccc;
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
            background-color: #0078D7;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
        }

        QPushButton#submitButton {
            background-color: #5CB85C;
        }

        QPushButton#submitButton:hover {
            background-color: #4CAE4C;
        }

        QPushButton#clearButton {
            background-color: #6c757d;
        }

        QPushButton#clearButton:hover {
            background-color: #5a6268;
        }
        QPushButton#updateButton {
            background-color: #007BFF;
        }
        QPushButton#updateButton:hover {
            background-color: #0056b3;
        }
        QPushButton#searchButton {
            background-color: #0078D7;
           
           
        }
        QPushButton#searchButton:hover {
            background-color: #0056b3;
        }

        QFrame#formFrame {
            border: 2px solid #0078D7;
            border-radius: 10px;
            padding: 15px;
            background-color: #ffffff;
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


# Run Application (For Testing)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentResultPage()
    window.show()
    sys.exit(app.exec_())
