import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

class GenerateFile(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate Result Files")
        self.setGeometry(100, 100, 400, 200)

        # Apply QSS Styling
        self.setStyleSheet(self.style_sheet())

        # Variables
        self.output_folder = ""

        # UI Elements
        self.title_label = QLabel("Generate Student Result Files")
        
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.folder_label = QLabel("Output Folder:")
        self.selected_folder_label = QLabel("No folder selected")
        self.select_folder_button = QPushButton("Select Folder")
        self.select_folder_button.clicked.connect(self.select_folder)

        self.roll_label = QLabel("Roll Number:")
        self.roll_input = QLineEdit()
        self.generate_single_button = QPushButton("Generate for Roll Number")
        self.generate_single_button.clicked.connect(self.generate_single_file)

        self.generate_all_button = QPushButton("Generate for All")
        self.generate_all_button.clicked.connect(self.generate_all_files)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.selected_folder_label)
        folder_layout.addWidget(self.select_folder_button)
        layout.addLayout(folder_layout)

        roll_layout = QHBoxLayout()
        roll_layout.addWidget(self.roll_label)
        roll_layout.addWidget(self.roll_input)
        roll_layout.addWidget(self.generate_single_button)
        layout.addLayout(roll_layout)

        layout.addWidget(self.generate_all_button)

        self.setLayout(layout)

    def style_sheet(self):
        return """
            QWidget {
                background-color: #f4f4f4;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                background-color: #fff;
                color: #333;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #003f6b;
            }
            #titleLabel {
                font-size: 22px;
                font-weight: bold;
                color: violet;
                margin-bottom: 18px;
                letter-spacing: 1px;
            }
        """
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.output_folder = folder
            self.selected_folder_label.setText(folder)

    def generate_single_file(self):
        roll_number = self.roll_input.text().strip()
        if not self.output_folder:
            QMessageBox.warning(self, "Warning", "Please select an output folder first.")
            return
        if not roll_number:
            QMessageBox.warning(self, "Warning", "Please enter a roll number.")
            return

        self.generate_file_for_roll(roll_number)

    def generate_all_files(self):
        if not self.output_folder:
            QMessageBox.warning(self, "Warning", "Please select an output folder first.")
            return

        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("SELECT roll FROM student")
            rolls = cur.fetchall()
            con.close()

            if not rolls:
                QMessageBox.information(self, "Info", "No students found in the database.")
                return

            for roll in rolls:
                self.generate_file_for_roll(roll[0])
            
            QMessageBox.information(self, "Success", "Successfully generated all result files.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def generate_file_for_roll(self, roll_number):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()

            cur.execute("SELECT name FROM student WHERE roll=?", (roll_number,))
            student_data = cur.fetchone()

            # Fetch all subjects, marks, grade, point for the student
            cur.execute("SELECT course, marks_ob, grade, gpa FROM result WHERE roll=?", (roll_number,))
            subjects_data = cur.fetchall()

            # Fetch CGPA for the student (assuming it's stored in a separate table or as an aggregate)
            cur.execute("SELECT DISTINCT(cpga) FROM result WHERE roll=?", (roll_number,))
            cgpa_data = cur.fetchone()

            con.close()

            if not student_data or not subjects_data:
                QMessageBox.warning(self, "Warning", f"No data found for roll number: {roll_number}")
                return

            student_name = student_data[0]
            file_content = """*************************************************************\n"""
            file_content += f"Name: {student_name}\n"
            file_content += f"Roll: {roll_number}\n"
            file_content += "---------------------------Mark sheet-------------------------\n"
            file_content += f"{'Subject':<12}{'Obtained Mark':<16}{'Grade Point':<14}{'Grade':<8}\n"
            file_content += "\n"
            for subject, marks_obtained, grade, point in subjects_data:
                file_content += f"{subject:<12}{str(marks_obtained):<16}{str(point):<14}{str(grade):<8}\n"
            file_content += "\n\nCGPA: "
            if cgpa_data:
                file_content += f"{cgpa_data[0]}\n"
            else:
                file_content += "N/A\n"
            file_content += "\n*************************************************************\n"

            file_path = f"{self.output_folder}/{roll_number}.txt"
            with open(file_path, "w") as f:
                f.write(file_content)
            
            if self.sender() == self.generate_single_button:
                QMessageBox.information(self, "Success", f"Successfully generated file for roll number: {roll_number}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while generating file for {roll_number}: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GenerateFile()
    window.show()
    sys.exit(app.exec_())

