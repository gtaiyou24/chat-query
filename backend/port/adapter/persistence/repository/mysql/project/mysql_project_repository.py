import uuid
from typing import override

from injector import inject

from modules.authority.domain.model.tenant.project import ProjectRepository, Project, ProjectId
from port.adapter.persistence.repository.mysql.project import CacheLayerProject


class MySQLProjectRepository(ProjectRepository):
    @inject
    def __init__(self, cache_layer_project: CacheLayerProject):
        self.__cache_layer_project = cache_layer_project

    @override
    def next_identity(self) -> ProjectId:
        return ProjectId(str(uuid.uuid4()))

    @override
    def add(self, project: Project) -> None:
        self.__cache_layer_project.set(project)
