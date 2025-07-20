import sys
import sqlite3
import yagmail
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

class SendEmail(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Send Result Email")
        self.setGeometry(100, 100, 500, 260)
        self.setStyleSheet("""
            QWidget { background-color: #f4f4f4; font-family: Arial, sans-serif; font-size: 14px; }
            QLabel { font-weight: bold; color: #333; }
            QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; background-color: #fff; color: #333; }
            QPushButton { background-color: #0078d7; color: white; border: none; border-radius: 5px; padding: 8px 15px; }
            QPushButton:hover { background-color: #005a9e; }
            QPushButton:pressed { background-color: #003f6b; }
            #titleLabel { font-size: 22px; font-weight: bold; color: violet; margin-bottom: 18px; letter-spacing: 1px; }
        """)

        self.title_label = QLabel("Send Student Result Email")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.from_email_label = QLabel("From Email:")
        self.from_email_input = QLineEdit("radoun086@gmail.com")
        self.app_password_label = QLabel("App Password:")
        self.app_password_input = QLineEdit("szsh yole rzcu jsei")
        self.app_password_input.setEchoMode(QLineEdit.Password)

        self.roll_label = QLabel("Roll Number:")
        self.roll_input = QLineEdit()
        self.email_label = QLabel("Email (leave blank to use student's email from DB):")
        self.email_input = QLineEdit()
        self.send_single_button = QPushButton("Send to Roll Number")
        self.send_single_button.clicked.connect(self.send_single_email)
        self.send_all_button = QPushButton("Send to All")
        self.send_all_button.clicked.connect(self.send_all_emails)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)

        from_layout = QHBoxLayout()
        from_layout.addWidget(self.from_email_label)
        from_layout.addWidget(self.from_email_input)
        layout.addLayout(from_layout)

        pass_layout = QHBoxLayout()
        pass_layout.addWidget(self.app_password_label)
        pass_layout.addWidget(self.app_password_input)
        layout.addLayout(pass_layout)

        roll_layout = QHBoxLayout()
        roll_layout.addWidget(self.roll_label)
        roll_layout.addWidget(self.roll_input)
        layout.addLayout(roll_layout)

        email_layout = QHBoxLayout()
        email_layout.addWidget(self.email_label)
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)

        layout.addWidget(self.send_single_button)
        layout.addWidget(self.send_all_button)
        self.setLayout(layout)

    def get_result_content(self, roll_number):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("SELECT name, email FROM student WHERE roll=?", (roll_number,))
            student_data = cur.fetchone()
            cur.execute("SELECT course, marks_ob, grade, gpa FROM result WHERE roll=?", (roll_number,))
            subjects_data = cur.fetchall()
            cur.execute("SELECT DISTINCT(cpga) FROM result WHERE roll=?", (roll_number,))
            cgpa_data = cur.fetchone()
            con.close()
            if not student_data or not subjects_data:
                return None, None, None
            student_name, student_email = student_data
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
            return file_content, student_name, student_email
        except Exception as e:
            return None, None, None

    def send_email(self, to_email, subject, content):
        sender_email = self.from_email_input.text().strip() or "radoun086@gmail.com"
        sender_password = self.app_password_input.text().strip() or "szsh yole rzcu jsei"
        try:
            yag = yagmail.SMTP(sender_email, sender_password)
            yag.send(to=to_email, subject=subject, contents=content)
            return True
        except Exception as e:
            return False

    def send_single_email(self):
        roll_number = self.roll_input.text().strip()
        to_email = self.email_input.text().strip()
        if not roll_number:
            QMessageBox.warning(self, "Warning", "Please enter a roll number.")
            return
        content, student_name, student_email = self.get_result_content(roll_number)
        if not content:
            QMessageBox.warning(self, "Warning", f"No data found for roll number: {roll_number}")
            return
        if not to_email:
            to_email = student_email
        if not to_email:
            QMessageBox.warning(self, "Warning", "No email address provided or found in database.")
            return
        subject = f"Result Sheet for {student_name} (Roll: {roll_number})"
        if self.send_email(to_email, subject, content):
            QMessageBox.information(self, "Success", f"Email sent to {to_email}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to send email to {to_email}")

    def send_all_emails(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("SELECT DISTINCT(roll) FROM student")
            rolls = cur.fetchall()
            con.close()
            if not rolls:
                QMessageBox.information(self, "Info", "No students found in the database.")
                return
            sent_count = 0
            for roll in rolls:
                roll_number = roll[0]
                content, student_name, student_email = self.get_result_content(roll_number)
                if content and student_email:
                    subject = f"Result Sheet for {student_name} (Roll: {roll_number})"
                    if self.send_email(student_email, subject, content):
                        sent_count += 1
            QMessageBox.information(self, "Success", f"Emails sent to {sent_count} students.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SendEmail()
    window.show()
    sys.exit(app.exec_())
