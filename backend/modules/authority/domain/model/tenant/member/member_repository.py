import abc

from modules.authority.domain.model.tenant.member import MemberId, Member


class MemberRepository(abc.ABC):
    @abc.abstractmethod
    def next_identity(self) -> MemberId:
        pass

    @abc.abstractmethod
    def save(self, member: Member) -> None:
        pass
