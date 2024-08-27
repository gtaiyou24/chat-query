from dataclasses import dataclass

from modules.authority.domain.model.tenant.member import Member
from modules.authority.domain.model.user import User, UserId


@dataclass(init=True, unsafe_hash=True, frozen=True)
class MemberDpo:
    member: Member
    user: User


@dataclass(init=True, unsafe_hash=True, frozen=True)
class MembersDpo:
    members: list[Member]
    users: set[User]

    @property
    def list_member_dpo(self) -> list[MemberDpo]:
        member_dpo_list = []
        for member in self.members:
            user = self.user_with_id(member.user_id)
            if user is None:
                continue
            dpo = MemberDpo(member, user)
            member_dpo_list.append(dpo)
        return member_dpo_list

    def user_with_id(self, user_id: UserId) -> User | None:
        for user in self.users:
            if user.id == user_id:
                return user
        return None
