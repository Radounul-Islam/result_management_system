
import sys
import create_db
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,  QHBoxLayout,
    QLabel, QStackedWidget, QVBoxLayout, QMessageBox, QPushButton
)

from dashboard import DashBoardWidget
from report import StudentReportUI
from result import StudentResultPage
from sidebar import SidebarWidget
from students import StudentDetailsUI

from create_db import create_db
from course import CourseManager


# Create the main window for the Student Management System
class StudentManagementUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 900, 600)
        create_db()
        self.initUI()
        self.setWindowTitle("Result Management System")
        
    
    def load_styles(self):
        return """
        QMainWindow {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
        
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
        
        #ExitButton {
            background-color:
            #ff0000;
            color: white;
            padding: 6px 20px;
            font-weight: bold;
            border-radius: 4px;
            }
        
        #ExitButton:hover {
            background-color:
            #cc0000;
           
         }
        

        """
    
    
    def exit_button_clicked(self):
        
    
     
        # Exit confirmation message box
        option = QMessageBox.question(
                self, "Exit Confirmation",
                "Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
        if option == QMessageBox.No:
                return
        self.close()

     
    

    def initUI(self):
        # Main Layout
        self.setStyleSheet(self.load_styles())
        main_widget = QWidget()
        # All layouts
        main_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()
        # Set the main layout to the central widget
        main_layout.addLayout(buttons_layout)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Sidebar (Navigation Menu)
        self.sidebar = SidebarWidget()
        #main_layout.addWidget(self.sidebar)
        buttons_layout.addWidget(self.sidebar)
       
        # Main Content Area
        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)

        
        # Exit Button 
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit_button_clicked)
        self.exit_button.setObjectName("ExitButton")
        buttons_layout.addWidget(self.exit_button)

        # Dashboard Page
        self.dashboard_page = DashBoardWidget()
        # Students Page
        self.students_page = StudentDetailsUI()
        
        # Course Page
        self.course_page = CourseManager()
        # Student Result Page
        self.result_page = StudentResultPage()
        # Student Report Page
        self.report_page = StudentReportUI()
        # Settings Page (Placeholder)
        self.settings_page = QLabel("Settings Page")

        pages = [self.dashboard_page, self.course_page, self.students_page,
                  self.result_page, self.report_page, self.settings_page]
        
        # Add pages to the stacked widget
        for page in pages:
            self.pages.addWidget(page)
        
        # Handle Sidebar Clicks
        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)
        
       
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentManagementUI()
    window.show()
    sys.exit(app.exec_())

