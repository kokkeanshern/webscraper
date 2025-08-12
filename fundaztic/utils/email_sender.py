import os
import smtplib
from email.mime.text import MIMEText


class Email:
    def __init__(self, subject, from_email, to_email, body):
        self.from_email = from_email
        self.msg = MIMEText(body, "html")
        self.msg["Subject"] = subject
        self.msg["From"] = from_email
        self.msg["To"] = to_email

    def send_email(self, email_provider):
        # smtp.gmail.com
        server = smtplib.SMTP(email_provider)
        server.starttls()
        server.login(self.from_email, os.environ["SERVICE_EMAIL_PASSWORD"])
        server.sendmail(self.msg.get("From"), self.msg["To"], self.msg.as_string())
        server.quit()
