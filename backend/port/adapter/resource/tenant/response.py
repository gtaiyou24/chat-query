from __future__ import annotations

from pydantic import BaseModel, Field

from modules.authority.application.tenant.dpo import TenantListDpo, ProjectListDpo
from modules.authority.domain.model.tenant import Tenant
from modules.authority.domain.model.tenant.project import Project


class TenantJson(BaseModel):
    id: str = Field(title="テナントID")
    name: str = Field(title="テナント名")

    @staticmethod
    def from_(tenant: Tenant) -> TenantJson:
        return TenantJson(id=tenant.id.value, name=tenant.name)


class TenantListJson(BaseModel):
    tenants: list[TenantJson]

    @staticmethod
    def from_(dpo: TenantListDpo) -> TenantListJson:
        return TenantListJson(tenants=[TenantJson.from_(tenant) for tenant in dpo.tenants])


class ProjectJson(BaseModel):
    id: str = Field(title="プロジェクトID")
    tenant_id: str = Field(title="テナントID")
    name: str = Field(title="プロジェクト名")

    @staticmethod
    def from_(project: Project) -> ProjectJson:
        return ProjectJson(id=project.id.value, tenant_id=project.tenant_id.value, name=project.name)


class ProjectListJson(BaseModel):
    projects: list[ProjectJson]

    @staticmethod
    def from_(dpo: ProjectListDpo) -> ProjectListJson:
        return ProjectListJson(projects=[ProjectJson.from_(project) for project in dpo.projects])
