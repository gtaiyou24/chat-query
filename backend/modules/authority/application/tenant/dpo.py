from dataclasses import dataclass

from modules.authority.domain.model.tenant import Tenant
from modules.authority.domain.model.tenant.project import Project


@dataclass(init=True, unsafe_hash=True, frozen=True)
class TenantListDpo:
    tenants: list[Tenant]


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ProjectListDpo:
    projects: list[Project]
