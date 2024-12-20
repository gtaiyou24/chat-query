import abc

from modules.authority.domain.model.user import EmailAddress


class MailDeliveryAdapter(abc.ABC):
    @abc.abstractmethod
    def send(self, to: EmailAddress, subject: str, html: str) -> None:
        pass
