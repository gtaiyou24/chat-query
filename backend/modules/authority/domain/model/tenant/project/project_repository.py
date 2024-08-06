import abc

from modules.authority.domain.model.tenant.project import ProjectId, Project


class ProjectRepository(abc.ABC):
    @abc.abstractmethod
    def next_identity(self) -> ProjectId:
        pass

    @abc.abstractmethod
    def add(self, project: Project) -> None:
        pass
