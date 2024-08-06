from modules.authority.domain.model.user import EmailAddress
from port.adapter.service.mail.adapter import MailDeliveryAdapter


class MailDeliveryAdapterStub(MailDeliveryAdapter):
    def send(self, to: EmailAddress, subject: str, html: str) -> None:
        print(f'send "{subject}" to {to.text}')
