from dataclasses import dataclass

from modules.authority.domain.model.tenant.member import Member


@dataclass(init=True, unsafe_hash=True, frozen=True)
class MemberDpo:
    member: Member


@dataclass(init=True, unsafe_hash=True, frozen=True)
class MembersDpo:
    members: list[Member]

    @property
    def list_member_dpo(self) -> list[MemberDpo]:
        return [MemberDpo(e) for e in self.members]
