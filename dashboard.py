
import sqlite3
from PyQt5.QtWidgets import (
    QApplication,QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QSizePolicy, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCursor

class DashBoardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.update_details()
        #self.buttons_clicked()

    def load_styles(self):
        return """
           QWidget {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
    }
        QMessageBox {
            background-color: #f5f5f5;
            font-family: Arial, sans-serif;
        }
        QMessageBox QLabel {
            background-color: #f5f5f5;
            font-size: 16px;
            font-weight: bold;
            color: #333;

        }
        QMessageBox QPushButton {
           color: black;
        }
        QMessageBox QPushButton:hover {
            background-color: #005A9E;
            color : white;
        }

        QFrame
        {
            background-color: #ccc;
            padding: 5px;
            border-radius: 10px;

        }
       
        QLabel {
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            margin: 0;
        }

        QLabel#studentCountLabel
        {
            background-color: #3498DB;
            
        }
        QLabel#attendanceRateLabel
        {
            background-color: #2ECC71;
         
        }
        QLabel#avgGradesLabel
        {
            background-color: #E74C3C;
          
        }

        QLabel#titleLabel{
        background-color: #002855;
        color: white;
        font-size: 22px;
        padding: 10px;
        border-radius: 5px;
        border: none;
        font-weight: bold;
    }
         
        """
    def initUI(self):
        self.setStyleSheet(self.load_styles())
        dashboard_layout = QVBoxLayout()
        dashboard_layout.setSpacing(5)
        title = QLabel("Student Result Management System")
        title.setObjectName("titleLabel")
        title.setFixedHeight(60)
        title.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(title)
  
        
        # background Image
        self.lbl_image = QLabel()
        self.image_path = "images/result.jpg"  # Change image path here
        pixmap = QPixmap(self.image_path)
        self.lbl_image.setPixmap(pixmap)
        
        self.lbl_image.setScaledContents(True)
        self.lbl_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        dashboard_layout.addWidget(self.lbl_image)
        # Set size policy to expand in both directions
     
        stats_frame = QFrame()
        stats_layout = QHBoxLayout()
        stats_frame.setLayout(stats_layout)


        self.student_count = QLabel(f"Total Courses:\n 0")
        self.attendance_rate = QLabel("Total Students:\n 0")
        self.avg_grades = QLabel("Total Results:\n 0")
        # For styling using css property
        self.student_count.setObjectName("studentCountLabel") 
        self.attendance_rate.setObjectName("attendanceRateLabel")
        self.avg_grades.setObjectName("avgGradesLabel")


        
        for label in [self.student_count, self.attendance_rate, self.avg_grades]:
            label.setAlignment(Qt.AlignCenter)
            stats_layout.addWidget(label)

        
        dashboard_layout.addWidget(stats_frame)
        self.setLayout(dashboard_layout)

   
    def update_details(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(DISTINCT cid)FROM course")
            cr = cur.fetchone()
            self.student_count.setText(f"Total Courses:\n {cr[0]}")
            cur.execute("SELECT COUNT(DISTINCT roll) FROM student")
            st = cur.fetchone()
            self.attendance_rate.setText(f"Total Students:\n {st[0]}")
            cur.execute("SELECT COUNT( * ) FROM result")
            rs = cur.fetchone()
            self.avg_grades.setText(f"Total Results:\n {rs[0]}")
            con.commit()
            con.close()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
            



def main()-> None:
    import sys
    app = QApplication([])
    dashboard = DashBoardWidget()
    dashboard.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()