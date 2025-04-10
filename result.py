import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QComboBox, QScrollArea, QFrame, QSizePolicy
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
        self.cmb_student.addItems(["Select", "Student 1", "Student 2", "Student 3"])
        
         # Placeholder search button
        self.btn_search = QPushButton("Search")
        self.btn_search.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_search.setObjectName("searchButton")

        # Student Name
        self.lbl_name = QLabel("Name")
        self.txt_name = QLineEdit()

        # Course Name
        self.lbl_course = QLabel("Course")
        self.txt_course = QLineEdit()

        # Marks Obtained
        self.lbl_marks_obtained = QLabel("Marks Obtained")
        self.txt_marks_obtained = QLineEdit()

        # Full Marks
        self.lbl_full_marks = QLabel("Full Marks")
        self.txt_full_marks = QLineEdit()

        # Submit & Clear Buttons
        self.btn_submit = QPushButton("Submit")
        self.btn_submit.setObjectName("submitButton")
        self.btn_clear = QPushButton("Clear")
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

       
    def load_student_details(self):
        pass
       
    def search_student(self):
        pass

    def clear_fields(self):
        self.cmb_student.setCurrentIndex(0)
        self.txt_name.clear()
        self.txt_course.clear()
        self.txt_marks_obtained.clear()
        self.txt_full_marks.clear()

    def submit_result(self):
        pass

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

        QPushButton:hover {
            background-color: #005A9E;
        }

        QPushButton#submitButton {
            background-color: #5CB85C;
        }

        QPushButton#submitButton:hover {
            background-color: #4CAE4C;
        }

        QPushButton#clearButton {
            background-color: #6C757D;
        }

        QPushButton#clearButton:hover {
            background-color: #5A6268;
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
