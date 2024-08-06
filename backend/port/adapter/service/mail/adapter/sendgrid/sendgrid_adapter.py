from modules.authority.domain.model.user import EmailAddress
from port.adapter.service.mail.adapter import MailDeliveryAdapter


class SendGridAdapter(MailDeliveryAdapter):
    """https://sendgrid.kke.co.jp/"""

    def send(self, to: EmailAddress, subject: str, html: str) -> None:
        raise NotImplementedError()
