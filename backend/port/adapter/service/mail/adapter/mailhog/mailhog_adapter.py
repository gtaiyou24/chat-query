import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from html2text import html2text

from modules.authority.domain.model.user import EmailAddress
from port.adapter.service.mail.adapter import MailDeliveryAdapter


class MailHogAdapter(MailDeliveryAdapter):
    def __init__(self):
        self.__smtp = smtplib.SMTP(host="mailhog", port=1025)
        self.__from = os.getenv('FROM_MAIL_ADDRESS')

    def send(self, to: EmailAddress, subject: str, html: str) -> None:
        mail = MIMEMultipart("alternative")
        mail["Subject"] = subject
        mail["From"] = self.__from
        mail["To"] = to.text

        mail.attach(MIMEText(html2text(html), "plain"))
        mail.attach(MIMEText(html, "html"))

        self.__smtp.sendmail(self.__from, to.text, mail.as_string())
