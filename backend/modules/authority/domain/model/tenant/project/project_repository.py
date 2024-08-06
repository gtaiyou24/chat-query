import abc

from modules.authority.domain.model.tenant.project import ProjectId


class ProjectRepository(abc.ABC):
    @abc.abstractmethod
    def next_identity(self) -> ProjectId:
        pass
