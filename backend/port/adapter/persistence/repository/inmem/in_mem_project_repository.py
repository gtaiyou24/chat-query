import uuid
from typing import override

from modules.authority.domain.model.tenant.project import ProjectRepository, Project, ProjectId


class InMemProjectRepository(ProjectRepository):
    projects: set[Project] = set()

    @override
    def next_identity(self) -> ProjectId:
        return ProjectId(str(uuid.uuid4()))

    @override
    def add(self, project: Project) -> None:
        self.projects.add(project)
