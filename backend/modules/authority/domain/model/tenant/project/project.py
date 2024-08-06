from __future__ import annotations

from dataclasses import dataclass

from modules.authority.domain.model.tenant.project import ProjectId


@dataclass(init=False, eq=False)
class Project:
    id: ProjectId
    name: str

    def __hash__(self):
        return hash(self.id.value)

    def __eq__(self, other: Project):
        if not isinstance(other, Project):
            return False
        return self.id == other.id
