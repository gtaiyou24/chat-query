import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from html2text import html2text

from modules.authority.domain.model.user import EmailAddress
from port.adapter.service.mail.adapter import MailDeliveryAdapter


class GmailAdapter(MailDeliveryAdapter):
    def __init__(self):
        self.__from = os.getenv('FROM_MAIL_ADDRESS')
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp.starttls()
        self.smtp.login(self.__from, os.getenv('GMAIL_SMTP_PASSWORD'))

    def send(self, to: EmailAddress, subject: str, html: str) -> None:
        mail = MIMEMultipart("alternative")
        mail["Subject"] = subject
        mail["From"] = self.__from
        mail["To"] = to.text

        mail.attach(MIMEText(html2text(html), "plain"))
        mail.attach(MIMEText(html, "html"))

        self.smtp.sendmail(self.__from, to.text, mail.as_string())
