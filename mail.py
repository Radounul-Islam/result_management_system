
from PyQt5.QtWidgets import (
   QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog
)
import yagmail

class MailSenderUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mail Sender")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(self.load_styles())

        # UI Elements
        self.recipient_label = QLabel("Recipient Email (comma-separated for group):")
        self.recipient_input = QLineEdit()

        self.subject_label = QLabel("Subject:")
        self.subject_input = QLineEdit()

        self.body_label = QLabel("Email Body:")
        self.body_input = QTextEdit()

        self.attachment_label = QLabel("Attachments:")
        self.attachment_input = QLineEdit()
        self.attachment_input.setReadOnly(True)
        self.browse_button = QPushButton("Browse")

        self.send_individual_button = QPushButton("Send to Individual")
        self.send_group_button = QPushButton("Send to Group")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.recipient_label)
        layout.addWidget(self.recipient_input)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.body_label)
        layout.addWidget(self.body_input)
        layout.addWidget(self.attachment_label)
        layout.addWidget(self.attachment_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.send_individual_button)
        layout.addWidget(self.send_group_button)

        self.setLayout(layout)

        # Button Actions
        self.browse_button.clicked.connect(self.browse_attachment)
        self.send_individual_button.clicked.connect(self.send_individual_email)
        self.send_group_button.clicked.connect(self.send_group_email)

        # Store attachments
        self.attachments = []

    def browse_attachment(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Attachments")
        if files:
            self.attachments.extend(files)
            self.attachment_input.setText(", ".join(self.attachments))

    def send_email(self, recipients):
        sender_email = "your_email@example.com"
        password = "your_password"

        subject = self.subject_input.text()
        body = self.body_input.toPlainText()

        try:
            yag = yagmail.SMTP(sender_email, password)
            yag.send(to=recipients, subject=subject, contents=[body] + self.attachments)
            QMessageBox.information(self, "Success", "Email sent successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send email: {e}")

    def send_individual_email(self):
        recipient = self.recipient_input.text().strip()
        if recipient:
            self.send_email([recipient])
        else:
            QMessageBox.warning(self, "Warning", "Please enter a recipient email.")

    def send_group_email(self):
        recipients = self.recipient_input.text().strip().split(",")
        recipients = [email.strip() for email in recipients if email.strip()]
        if recipients:
            self.send_email(recipients)
        else:
            QMessageBox.warning(self, "Warning", "Please enter at least one recipient email.")

    def load_styles(self):
        return """
        QWidget {
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }

        QLabel {
            color: #333;
        }

        QLineEdit, QTextEdit {
            border: 1px solid #ccc;
            padding: 5px;
            border-radius: 4px;
        }

        QPushButton {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
          
        }

        QPushButton:hover {
            background-color: #0056b3;
        }
        
        """
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MailSenderUI()
    window.show()
    sys.exit(app.exec_())