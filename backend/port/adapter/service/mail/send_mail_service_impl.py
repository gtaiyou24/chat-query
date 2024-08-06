from injector import inject
from typing import override

from modules.authority.domain.model.mail import SendMailService
from modules.authority.domain.model.user import EmailAddress
from port.adapter.service.mail.adapter import MailDeliveryAdapter


class SendMailServiceImpl(SendMailService):
    @inject
    def __init__(self, mail_delivery_adapter: MailDeliveryAdapter):
        self.__mail_delivery_adapter = mail_delivery_adapter

    @override
    def send(self, to: EmailAddress, subject: str, html: str) -> None:
        self.__mail_delivery_adapter.send(to, subject, html)
