import yagmail

yag = yagmail.SMTP("your_email@example.com", "your_password")
yag.send(
    to="receiver_email@example.com",
    subject="Test Email",
    contents="This is a test email sent using yagmail."
)
print("Email sent successfully!")