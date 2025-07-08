
import sys
from PyQt5.QtWidgets import QListWidget, QApplication
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

class SidebarWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setStyleSheet(self.laod_stylesheet())
        self.addItem("Dashboard")
        self.addItem("Course")
        self.addItem("Student")
        self.addItem("Result")
        self.addItem("View Result")

        self.addItem("Generate Result Files")
      
        self.setFixedWidth(220)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def laod_stylesheet(self):
        return """
            QListWidget {
                background-color: #34495E;
                color: #ffffff;
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
            QListWidget::item {
                background-color: #03fcf4;
                padding: 10px;
                border-radius: 5px;
                margin: 5px;
                color: #333;
            }
            QListWidget::item:selected {
                background-color: #03fc6f;
                color: white;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #fc03f4;
                color: #ECF0F1;
            }
""" 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    sidebar = SidebarWidget()
    sidebar.show()
    sys.exit(app.exec_())
#         self.dashboard_page.setLayout(dashboard_layout)
